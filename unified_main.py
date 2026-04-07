from fastapi import FastAPI, UploadFile, File, HTTPException, Body, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from PIL import Image
import io
import os
import re
import time
import uuid
import asyncio
import urllib.request
import logging
import sys
from typing import List, Optional
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Image_to_Text_description_generator_main'))
# -------------------- Logging --------------------
def configure_logging(level: int = logging.INFO) -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if getattr(handler, "_custom", False):
            return
    root_logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    handler._custom = True
    root_logger.setLevel(level)
    root_logger.addHandler(handler)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

configure_logging()
logger = logging.getLogger("UnifiedBackend")

# -------------------- Lazy imports (heavy ML deps) --------------------
# These are imported at startup or on first request to avoid crashes
# if one service's deps aren't installed.

from Image_to_Text_description_generator_main.app.logger import get_logger
from Image_to_Text_description_generator_main.app.description_generator import generate_description
from Image_to_Text_description_generator_main.app.config import SUPPORTED_LANGUAGES

log = get_logger(__name__)

# Color mismatch components — initialized at startup
_detector = None
_agent = None

def get_color_components():
    global _detector, _agent
    if _detector is None or _agent is None:
        from ProductColorMismatch.src.clip_color_detector import ClipColorDetector
        from ProductColorMismatch.src.color_match_agent import ColorMatchAgent
        logger.info("Initializing ClipColorDetector and ColorMatchAgent...")
        _detector = ClipColorDetector()
        _agent = ColorMatchAgent(openai_api_key=os.getenv("OPENAI_API_KEY"))
        logger.info("Color components initialized.")
    return _detector, _agent

# -------------------- App Setup --------------------
app = FastAPI(title="Unified E-Commerce Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://e-commerce-gilt-kappa.vercel.app",
        "*",  # remove this if you want to lock down CORS
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Startup --------------------
@app.on_event("startup")
async def startup_event():
    # Vision backend preload
    backend = os.environ.get("VISION_BACKEND", "gpt4o").lower()
    log.info("startup | VISION_BACKEND=%s", backend)
    if backend == "minicpm":
        try:
            from Image_to_Text_description_generator_main.app.vision_minicpm import load_backend
            load_backend()
            log.info("startup | MiniCPM-V preloaded successfully")
        except Exception as e:
            log.warning("startup | Could not preload MiniCPM-V: %s", e)
    else:
        log.info("startup | Using %s backend (no preloading needed)", backend)

    # Color components preload
    try:
        get_color_components()
    except Exception as e:
        logger.warning("startup | Could not preload color components: %s", e)

# -------------------- Shared Utils --------------------
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/temp", StaticFiles(directory=UPLOAD_DIR), name="temp")

async def run_blocking(fn, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fn, *args)

# -------------------- Azure Blob Config (Color Mismatch) --------------------
AZURE_ACCOUNT   = "ecommerceblobvtryon"
AZURE_CONTAINER = "vtryon"
AZURE_FOLDER    = "Product_Colour_MisMatch"
BLOB_BASE_URL   = f"https://{AZURE_ACCOUNT}.blob.core.windows.net/{AZURE_CONTAINER}/{AZURE_FOLDER}"

OUTPUT_CSV_PATH = os.path.join(
    os.path.dirname(__file__), "ProductColorMismatch", "data", "hf_products_with_verdict.csv"
)
COLOR_COLUMN_CANDIDATES = ["baseColour", "base_colour", "color", "colour"]
NAME_COLUMN_CANDIDATES  = ["productDisplayName", "product_name", "name", "title"]

def sanitize_id(raw: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(raw))
    return safe or "unknown"

def get_blob_image_url(product_id: str, index: Optional[int] = None) -> Optional[str]:
    safe_id = sanitize_id(product_id)
    candidates = []
    if index is not None:
        candidates += [
            f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.jpg",
            f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.png",
            f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.jpeg",
        ]
    candidates += [
        f"{BLOB_BASE_URL}/{safe_id}.jpg",
        f"{BLOB_BASE_URL}/{safe_id}.png",
        f"{BLOB_BASE_URL}/{safe_id}.jpeg",
    ]
    for url in candidates:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    return url
        except Exception:
            continue
    fallback = (
        f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.jpg"
        if index is not None
        else f"{BLOB_BASE_URL}/{safe_id}.jpg"
    )
    logger.warning("Blob not found for product_id=%s, index=%s. Fallback: %s", product_id, index, fallback)
    return fallback

# ==================================================
# ROOT / HEALTH
# ==================================================

@app.get("/")
@app.head("/")
async def root():
    return {
        "status": "ok",
        "service": "Unified E-Commerce Backend",
        "vision_backend": os.environ.get("VISION_BACKEND", "gpt4o"),
        "routes": {
            "image_to_text": "/image-to-text/...",
            "color_mismatch": "/color/...",
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "unified"}

# ==================================================
# IMAGE-TO-TEXT ROUTES  (previously port 8010)
# ==================================================

@app.get("/image-to-text/kpis")
async def get_kpis():
    return {
        "kpis": [
            {"label": "Language Completeness",  "value": "87%",    "icon": "Languages",   "change": 12},
            {"label": "Marketplace Readiness",  "value": "94/100", "icon": "Target",      "change": 5},
            {"label": "SEO Quality Score",       "value": "91/100", "icon": "Zap",         "change": 8},
            {"label": "Attribute Accuracy",      "value": "96%",    "icon": "CheckCircle", "change": 3},
            {"label": "Time Saved/Listing",      "value": "4.2min", "icon": "Clock",       "change": -22},
        ]
    }

@app.post("/image-to-text/upload")
async def upload_image(file: UploadFile = File(...), sku: str = None):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_id = f"img-{uuid.uuid4().hex[:8]}"
    extension = os.path.splitext(file.filename)[1].lower() or ".jpeg"
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{extension}")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    with open(file_path, "wb") as f:
        f.write(contents)

    base_url = (
        os.environ.get("RENDER_EXTERNAL_URL")
        or os.environ.get("BASE_URL")
        or "http://localhost:8000"
    ).rstrip("/")

    log.info("upload | success | image_id=%s filename=%s", file_id, file.filename)
    return {
        "success": True,
        "imageId": file_id,
        "url": f"{base_url}/temp/{file_id}{extension}",
        "filename": file.filename,
        "sku": sku,
    }

@app.post("/generate-description")
async def generate_description_endpoint(
    image: UploadFile = File(...),
    language: str = Form(None),
):
    if not image.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    language = language or "en"
    if language not in SUPPORTED_LANGUAGES.values():
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")

    file_id = f"temp-{uuid.uuid4().hex[:8]}"
    extension = os.path.splitext(image.filename)[1].lower() or ".jpeg"
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{extension}")

    contents = await image.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    with open(file_path, "wb") as f:
        f.write(contents)

    t0 = time.perf_counter()
    try:
        ai_result = await run_blocking(generate_description, file_path, language)
        log.info("generate_description | success | elapsed=%.2fs", time.perf_counter() - t0)
        return {
            "title":             ai_result.get("title", ""),
            "short_description": ai_result.get("short_description", ""),
            "long_description":  ai_result.get("long_description", ""),
            "bullet_points":     ai_result.get("bullet_points", []),
            "attributes":        ai_result.get("attributes", {}),
        }
    except Exception as e:
        log.error("generate_description | failed | error=%s", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/image-to-text/generate")
async def generate_product_text(payload: dict = Body(...)):
    image_id = payload.get("imageId")
    language = payload.get("language", "en")
    extension = payload.get("extension", ".jpeg")

    image_path = os.path.join(UPLOAD_DIR, f"{image_id}{extension}")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    result = generate_description(image_path, language)
    return {
        "success": True,
        "title":            result.get("title"),
        "shortDescription": result.get("short_description"),
        "bulletPoints":     result.get("bullet_points", []),
        "attributes":       result.get("attributes", {}),
    }

@app.get("/image-to-text/translations/{image_id}")
async def get_translations(image_id: str, language: str = None):
    files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(image_id)]
    if not files:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = os.path.join(UPLOAD_DIR, files[0])
    translations = []
    for lang in SUPPORTED_LANGUAGES:
        if language and lang != language:
            continue
        result = generate_description(file_path, lang)
        translations.append({
            "code":        lang,
            "title":       result.get("title"),
            "description": result.get("short_description"),
        })
    return {"imageId": image_id, "translations": translations}

@app.get("/image-to-text/quality-check/{image_id}")
async def get_quality_check(image_id: str):
    files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(image_id)]
    if not files:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"imageId": image_id, "qualityChecks": []}

@app.post("/image-to-text/approve")
async def approve_translations(payload: dict = Body(...)):
    languages: List[str] = payload.get("languages") or []
    return {
        "success": True,
        "approved": len(languages) if languages else len(SUPPORTED_LANGUAGES),
    }

# ==================================================
# COLOR MISMATCH ROUTES  (previously port 8020)
# All prefixed with /color
# ==================================================

@app.get("/color/health")
def color_health():
    return {"status": "ok", "mode": "gpt-vision-only"}

@app.get("/color/image/{product_id}")
def get_product_image(product_id: str, index: Optional[int] = Query(None)):
    blob_url = get_blob_image_url(product_id, index)
    if blob_url is None:
        raise HTTPException(status_code=404, detail=f"Image not found for product ID: {product_id}")
    return RedirectResponse(url=blob_url)

@app.get("/color/dataset")
def get_dataset():
    if not os.path.exists(OUTPUT_CSV_PATH):
        raise HTTPException(status_code=404, detail=f"Output CSV not found at: {OUTPUT_CSV_PATH}")

    df = pd.read_csv(OUTPUT_CSV_PATH)
    if df.empty:
        raise HTTPException(status_code=400, detail="Dataset is empty.")

    color_col = next((c for c in COLOR_COLUMN_CANDIDATES if c in df.columns), None)
    if color_col is None:
        raise HTTPException(status_code=400, detail="Could not find a color column.")

    name_col = next((c for c in NAME_COLUMN_CANDIDATES if c in df.columns), None)

    records = df.where(pd.notnull(df), None).to_dict(orient="records")
    for i, row in enumerate(records):
        product_id = str(row.get("id") or row.get("product_id") or i)
        row["image_url"] = get_blob_image_url(product_id, index=i)

    return {
        "rows": records,
        "color_column": color_col,
        "name_column": name_col,
    }

@app.post("/color/detect-color")
async def detect_color(
    file: UploadFile = File(...),
    top_k: int = Form(3),
    confidence_threshold: float = Form(0.25),
):
    detector, _ = get_color_components()
    img_bytes = await file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    result = detector.detect_color(
        image=image,
        candidate_colors=None,
        top_k=top_k,
        confidence_threshold=confidence_threshold,
    )
    return result

@app.post("/color/match-color")
async def match_color(
    expected_color: str = Form(...),
    detected_color: str = Form(...),
):
    _, agent = get_color_components()
    verdict = agent.get_verdict(expected_color, detected_color)
    return {
        "expected_color": expected_color,
        "detected_color": detected_color,
        "verdict": verdict,
    }

@app.post("/color/detect-and-match")
async def detect_and_match(
    file: UploadFile = File(...),
    expected_color: str = Form(...),
):
    detector, agent = get_color_components()
    img_bytes = await file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    det = detector.detect_color(image=image)
    verdict = agent.get_verdict(
        expected_color=expected_color,
        detected_color=det["detected_color"]
    )
    return {
        "detection": det,
        "expected_color": expected_color,
        "verdict": verdict,
    }

# -------------------- Executive Dashboard Endpoints --------------------
# Import executive endpoints from mismatch_backend.py
try:
    from mismatch_backend import (
        executive_kpis,
        executive_alerts,
        executive_photoshoot_stats,
        executive_risk_radar,
        photoshoot_performance
    )
    
    # Register the executive endpoints
    app.get("/executive/kpis")(executive_kpis)
    app.get("/executive/alerts")(executive_alerts)
    app.get("/executive/ai-photoshoot-stats")(executive_photoshoot_stats)
    app.get("/executive/risk-radar")(executive_risk_radar)
    app.get("/executive/photoshoot-performance")(photoshoot_performance)
    
    logger.info("Executive dashboard endpoints loaded successfully")
except Exception as e:
    logger.warning(f"Could not load executive endpoints: {e}")

# -------------------- Local Run --------------------
if __name__ == "__main__":
    import uvicorn
    configure_logging()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("unified_main:app", host="0.0.0.0", port=port, reload=True)
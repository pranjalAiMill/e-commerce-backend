from fastapi import FastAPI, UploadFile, File, HTTPException, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import time
import uuid
import asyncio
from typing import List

from app.logger import get_logger
from app.description_generator import generate_description
from app.config import SUPPORTED_LANGUAGES

log = get_logger(__name__)

# -------------------- App Setup --------------------
app = FastAPI(title="Image-to-Text Vision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://e-commerce-gilt-kappa.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Startup --------------------
@app.on_event("startup")
async def startup_event():
    backend = os.environ.get("VISION_BACKEND", "gpt4o").lower()
    log.info("startup | VISION_BACKEND=%s", backend)

    if backend == "minicpm":
        log.info("startup | Preloading MiniCPM-V model...")
        try:
            from app.vision_minicpm import load_backend
            load_backend()
            log.info("startup | MiniCPM-V model preloaded successfully")
        except Exception as e:
            log.warning(
                "startup | Could not preload MiniCPM-V: %s; will load on first request", e
            )
    else:
        log.info("startup | Using %s backend (no preloading needed)", backend)

# -------------------- Utils --------------------
async def run_blocking(fn, *args):
    """
    Run blocking CPU/IO work in a threadpool.
    This prevents Render from killing long requests.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fn, *args)

# -------------------- Storage --------------------
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/temp", StaticFiles(directory=UPLOAD_DIR), name="temp")

# -------------------- Endpoints --------------------

@app.get("/health")
async def health():
    log.info("health | GET /health")
    return {"status": "ok", "service": "image-to-text"}

@app.get("/")
@app.head("/")
async def root():
    log.info("root | GET /")
    return {
        "status": "ok",
        "service": "Image-to-Text Vision API",
        "backend": os.environ.get("VISION_BACKEND", "gpt4o"),
    }

# 1️⃣ KPIs
@app.get("/image-to-text/kpis")
async def get_kpis():
    log.info("kpis | GET /image-to-text/kpis")
    return {
        "kpis": [
            {"label": "Language Completeness", "value": "87%", "icon": "Languages", "change": 12},
            {"label": "Marketplace Readiness", "value": "94/100", "icon": "Target", "change": 5},
            {"label": "SEO Quality Score", "value": "91/100", "icon": "Zap", "change": 8},
            {"label": "Attribute Accuracy", "value": "96%", "icon": "CheckCircle", "change": 3},
            {"label": "Time Saved/Listing", "value": "4.2min", "icon": "Clock", "change": -22},
        ]
    }

# 2️⃣ Upload Image
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
        or "http://localhost:8010"
    ).rstrip("/")

    log.info("upload | success | image_id=%s filename=%s", file_id, file.filename)

    return {
        "success": True,
        "imageId": file_id,
        "url": f"{base_url}/temp/{file_id}{extension}",
        "filename": file.filename,
        "sku": sku,
    }

# 2.5️⃣ Generate Description (FIXED – Render safe)
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

    log.info("generate_description | start | filename=%s language=%s", image.filename, language)
    t0 = time.perf_counter()

    try:
        # 🔴 ONLY FIX IS HERE
        ai_result = await run_blocking(generate_description, file_path, language)

        elapsed = time.perf_counter() - t0
        log.info(
            "generate_description | success | filename=%s language=%s elapsed_sec=%.2f",
            image.filename,
            language,
            elapsed,
        )

        return {
            "title": ai_result.get("title", ""),
            "short_description": ai_result.get("short_description", ""),
            "long_description": ai_result.get("long_description", ""),
            "bullet_points": ai_result.get("bullet_points", []),
            "attributes": ai_result.get("attributes", {}),
        }

    except Exception as e:
        elapsed = time.perf_counter() - t0
        log.error(
            "generate_description | failed | filename=%s language=%s elapsed_sec=%.2f error=%s",
            image.filename,
            language,
            elapsed,
            e,
        )
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# 3️⃣ Generate Product Description 
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
        "title": result.get("title"),
        "shortDescription": result.get("short_description"),
        "bulletPoints": result.get("bullet_points", []),
        "attributes": result.get("attributes", {}),
    }

# 4️⃣ Translations 
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
            "code": lang,
            "title": result.get("title"),
            "description": result.get("short_description"),
        })

    return {"imageId": image_id, "translations": translations}

# 5️⃣ Quality Check 
@app.get("/image-to-text/quality-check/{image_id}")
async def get_quality_check(image_id: str):
    files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(image_id)]
    if not files:
        raise HTTPException(status_code=404, detail="Image not found")

    return {"imageId": image_id, "qualityChecks": []}

# 6️⃣ Approve Translations 
@app.post("/image-to-text/approve")
async def approve_translations(payload: dict = Body(...)):
    languages: List[str] = payload.get("languages") or []
    return {
        "success": True,
        "approved": len(languages) if languages else len(SUPPORTED_LANGUAGES),
    }

# -------------------- Local Run --------------------
if __name__ == "__main__":
    import uvicorn
    from app.logger import configure_logging

    configure_logging()
    port = int(os.environ.get("PORT", 8010))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)



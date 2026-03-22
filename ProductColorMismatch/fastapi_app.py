# # from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import FileResponse
# # from PIL import Image
# # import io
# # import os
# # import re
# # from typing import Optional, List
# # import uvicorn
# # from dotenv import load_dotenv
# # import pandas as pd
# # load_dotenv()


# # from src.clip_color_detector import ClipColorDetector
# # from src.color_match_agent import ColorMatchAgent


# # app = FastAPI(title="Product Color Detection API")
# # IMAGE_DIR = "data/images"

# # # Allow frontend calls (Streamlit etc.)
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # OUTPUT_CSV_PATH = "data/hf_products_with_verdict.csv"
# # COLOR_COLUMN_CANDIDATES = ["baseColour", "base_colour", "color", "colour"]
# # NAME_COLUMN_CANDIDATES = ["productDisplayName", "product_name", "name", "title"]


# # def sanitize_id(raw: str) -> str:
# #     """Sanitize ID for filename matching."""
# #     safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(raw))
# #     return safe or "unknown"


# # def get_image_path(product_id: str, index: Optional[int] = None) -> Optional[str]:
# #     """
# #     Find image path for a product ID.
# #     Looks for pattern: {index:05d}_{id}.{ext}
# #     """
# #     safe_id = sanitize_id(product_id)
    
# #     # Try exact match with index if provided
# #     if index is not None:
# #         expected_name = f"{index:05d}_{safe_id}.jpg"
# #         path = os.path.join(IMAGE_DIR, expected_name)
# #         if os.path.exists(path):
# #             return path
        
# #         # Try with different extensions
# #         for ext in [".jpg", ".jpeg", ".png"]:
# #             path = os.path.join(IMAGE_DIR, f"{index:05d}_{safe_id}{ext}")
# #             if os.path.exists(path):
# #                 return path
        
# #         # Try prefix match
# #         prefix = f"{index:05d}_"
# #         if os.path.exists(IMAGE_DIR):
# #             for fname in os.listdir(IMAGE_DIR):
# #                 if fname.startswith(prefix) and fname.lower().endswith((".jpg", ".jpeg", ".png")):
# #                     return os.path.join(IMAGE_DIR, fname)
    
# #     # Fallback: search by ID in filename
# #     if os.path.exists(IMAGE_DIR):
# #         for fname in os.listdir(IMAGE_DIR):
# #             if safe_id in fname and fname.lower().endswith((".jpg", ".jpeg", ".png")):
# #                 return os.path.join(IMAGE_DIR, fname)
    
# #     return None

# # # Instantiate components (kept intact)
# # detector = ClipColorDetector(
# #     device="cpu",
# #     enable_gpt_fallback=True,
# # )

# # agent = ColorMatchAgent(
# #     openai_api_key=os.getenv("OPENAI_API_KEY"),
# # )


# # @app.get("/health")
# # def health():
# #     return {"status": "ok"}


# # @app.get("/image/{product_id}")
# # def get_product_image(product_id: str, index: Optional[int] = Query(None)):
# #     """
# #     Serve product image by product ID.
# #     Optional query param: index (row index in CSV)
# #     """
# #     img_path = get_image_path(product_id, index)
    
# #     if img_path is None or not os.path.exists(img_path):
# #         raise HTTPException(
# #             status_code=404,
# #             detail=f"Image not found for product ID: {product_id}",
# #         )
    
# #     # Determine media type
# #     ext = os.path.splitext(img_path)[1].lower()
# #     media_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    
# #     return FileResponse(img_path, media_type=media_type)


# # @app.get("/dataset")
# # def get_dataset():
# #     """
# #     Browse the processed dataset used by the Streamlit app.

# #     Returns JSON with:
# #     - rows: list of product records
# #     - color_column: which column contains the catalog color
# #     - name_column: which column contains the product name (if any)
# #     """
# #     if not os.path.exists(OUTPUT_CSV_PATH):
# #         raise HTTPException(
# #             status_code=404,
# #             detail=f"Output CSV not found at: {OUTPUT_CSV_PATH}",
# #         )

# #     df = pd.read_csv(OUTPUT_CSV_PATH)

# #     if df.empty:
# #         raise HTTPException(
# #             status_code=400,
# #             detail="Dataset is empty. Run the pipeline first to generate the CSV.",
# #         )

# #     color_col = next(
# #         (c for c in COLOR_COLUMN_CANDIDATES if c in df.columns),
# #         None,
# #     )
# #     if color_col is None:
# #         raise HTTPException(
# #             status_code=400,
# #             detail=(
# #                 "Could not find a color column. "
# #                 "Expected one of: baseColour, base_colour, color, colour."
# #             ),
# #         )

# #     for col in ["detected_color", "detected_confidence", "Verdict"]:
# #         if col not in df.columns:
# #             raise HTTPException(
# #                 status_code=400,
# #                 detail=f"Missing required column in CSV: '{col}'",
# #             )

# #     name_col = next(
# #         (c for c in NAME_COLUMN_CANDIDATES if c in df.columns),
# #         None,
# #     )

# #     # Convert NaN to None so JSON is clean
# #     records = df.where(pd.notnull(df), None).to_dict(orient="records")

# #     return {
# #         "rows": records,
# #         "color_column": color_col,
# #         "name_column": name_col,
# #     }


# # @app.post("/detect-color")
# # async def detect_color(
# #     file: UploadFile = File(...),
# #     top_k: int = Form(3),
# #     confidence_threshold: float = Form(0.25),
# # ):
# #     img_bytes = await file.read()
# #     image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

# #     result = detector.detect_color(
# #         image=image,
# #         candidate_colors=None,
# #         top_k=top_k,
# #         confidence_threshold=confidence_threshold,
# #     )

# #     return result


# # @app.post("/match-color")
# # async def match_color(
# #     expected_color: str = Form(...),
# #     detected_color: str = Form(...),
# # ):
# #     verdict = agent.get_verdict(expected_color, detected_color)
# #     return {
# #         "expected_color": expected_color,
# #         "detected_color": detected_color,
# #         "verdict": verdict,
# #     }


# # @app.post("/detect-and-match")
# # async def detect_and_match(
# #     file: UploadFile = File(...),
# #     expected_color: str = Form(...),
# # ):
# #     img_bytes = await file.read()
# #     image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

# #     det = detector.detect_color(image=image)

# #     verdict = agent.get_verdict(
# #         expected_color=expected_color,
# #         detected_color=det["detected_color"],
# #     )

# #     return {
# #         "detection": det,
# #         "expected_color": expected_color,
# #         "verdict": verdict,
# #     }
# # if __name__ == "__main__":
# #     uvicorn.run(
# #         "fastapi_app:app",
# #         host="0.0.0.0",
# #         port=8020,
# #         reload=True
# #     )































# from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from PIL import Image
# import io
# import os
# import re
# from typing import Optional, List
# import uvicorn
# from dotenv import load_dotenv
# import pandas as pd
# load_dotenv()

# # Import the updated detector
# from src.clip_color_detector import ClipColorDetector
# from src.color_match_agent import ColorMatchAgent

# app = FastAPI(title="Product Color Detection API (GPT Only)")
# IMAGE_DIR = "data/images"

# # Allow frontend calls (Streamlit etc.)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# OUTPUT_CSV_PATH = "data/hf_products_with_verdict.csv"
# COLOR_COLUMN_CANDIDATES = ["baseColour", "base_colour", "color", "colour"]
# NAME_COLUMN_CANDIDATES = ["productDisplayName", "product_name", "name", "title"]

# def sanitize_id(raw: str) -> str:
#     """Sanitize ID for filename matching."""
#     safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(raw))
#     return safe or "unknown"

# def get_image_path(product_id: str, index: Optional[int] = None) -> Optional[str]:
#     """Find image path for a product ID."""
#     safe_id = sanitize_id(product_id)
    
#     if index is not None:
#         expected_name = f"{index:05d}_{safe_id}.jpg"
#         path = os.path.join(IMAGE_DIR, expected_name)
#         if os.path.exists(path):
#             return path
        
#         for ext in [".jpg", ".jpeg", ".png"]:
#             path = os.path.join(IMAGE_DIR, f"{index:05d}_{safe_id}{ext}")
#             if os.path.exists(path):
#                 return path
        
#         prefix = f"{index:05d}_"
#         if os.path.exists(IMAGE_DIR):
#             for fname in os.listdir(IMAGE_DIR):
#                 if fname.startswith(prefix) and fname.lower().endswith((".jpg", ".jpeg", ".png")):
#                     return os.path.join(IMAGE_DIR, fname)
    
#     if os.path.exists(IMAGE_DIR):
#         for fname in os.listdir(IMAGE_DIR):
#             if safe_id in fname and fname.lower().endswith((".jpg", ".jpeg", ".png")):
#                 return os.path.join(IMAGE_DIR, fname)
    
#     return None

# # --- INSTANTIATE COMPONENTS ---
# # Updated: No device arg, no enable_fallback arg needed
# detector = ClipColorDetector() 

# agent = ColorMatchAgent(
#     openai_api_key=os.getenv("OPENAI_API_KEY"),
# )

# @app.get("/health")
# def health():
#     return {"status": "ok", "mode": "gpt-vision-only"}

# @app.get("/image/{product_id}")
# def get_product_image(product_id: str, index: Optional[int] = Query(None)):
#     img_path = get_image_path(product_id, index)
    
#     if img_path is None or not os.path.exists(img_path):
#         raise HTTPException(
#             status_code=404,
#             detail=f"Image not found for product ID: {product_id}",
#         )
    
#     ext = os.path.splitext(img_path)[1].lower()
#     media_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    
#     return FileResponse(img_path, media_type=media_type)

# @app.get("/dataset")
# def get_dataset():
#     if not os.path.exists(OUTPUT_CSV_PATH):
#         raise HTTPException(
#             status_code=404,
#             detail=f"Output CSV not found at: {OUTPUT_CSV_PATH}",
#         )

#     df = pd.read_csv(OUTPUT_CSV_PATH)

#     if df.empty:
#         raise HTTPException(
#             status_code=400,
#             detail="Dataset is empty.",
#         )

#     color_col = next(
#         (c for c in COLOR_COLUMN_CANDIDATES if c in df.columns),
#         None,
#     )
#     if color_col is None:
#         raise HTTPException(
#             status_code=400,
#             detail="Could not find a color column.",
#         )

#     name_col = next(
#         (c for c in NAME_COLUMN_CANDIDATES if c in df.columns),
#         None,
#     )

#     records = df.where(pd.notnull(df), None).to_dict(orient="records")

#     return {
#         "rows": records,
#         "color_column": color_col,
#         "name_column": name_col,
#     }

# @app.post("/detect-color")
# async def detect_color(
#     file: UploadFile = File(...),
#     top_k: int = Form(3),
#     confidence_threshold: float = Form(0.25),
# ):
#     img_bytes = await file.read()
#     image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

#     # Call detector (arguments ignored by GPT impl but passed for safety)
#     result = detector.detect_color(
#         image=image,
#         candidate_colors=None,
#         top_k=top_k,
#         confidence_threshold=confidence_threshold,
#     )

#     return result

# @app.post("/match-color")
# async def match_color(
#     expected_color: str = Form(...),
#     detected_color: str = Form(...),
# ):
#     verdict = agent.get_verdict(expected_color, detected_color)
#     return {
#         "expected_color": expected_color,
#         "detected_color": detected_color,
#         "verdict": verdict,
#     }

# @app.post("/detect-and-match")
# async def detect_and_match(
#     file: UploadFile = File(...),
#     expected_color: str = Form(...),
# ):
#     img_bytes = await file.read()
#     image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

#     det = detector.detect_color(image=image)

#     verdict = agent.get_verdict(
#         expected_color=expected_color,
#         detected_color=det["detected_color"],
#     )

#     return {
#         "detection": det,
#         "expected_color": expected_color,
#         "verdict": verdict,
#     }

# if __name__ == "__main__":
#     uvicorn.run(
#         "fastapi_app:app",
#         host="0.0.0.0",
#         port=8020,
#         reload=True
#     )


# @app.get("/")
# def home():
#     return {"message": "Server is running! Go to /docs to test the API."}


# from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from PIL import Image
# import io
# import os
# import re
# from typing import Optional, List
# import uvicorn
# from dotenv import load_dotenv
# import pandas as pd
# load_dotenv()

# # ==================================================
# # LOGGING — must be first, before other imports
# # ==================================================
# import logging
# import sys

# def configure_logging(level: int = logging.INFO) -> None:
#     root_logger = logging.getLogger()
#     for handler in root_logger.handlers:
#         if getattr(handler, "_custom", False):
#             return
#     root_logger.handlers.clear()
#     handler = logging.StreamHandler(sys.stdout)
#     handler.setFormatter(logging.Formatter(
#         fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     ))
#     handler._custom = True
#     root_logger.setLevel(level)
#     root_logger.addHandler(handler)
#     logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
#     logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
#     logging.getLogger("watchfiles").setLevel(logging.WARNING)

# configure_logging()
# logger = logging.getLogger("ColorDetection-Backend")

# # ==================================================
# # APP IMPORTS (after logging)
# # ==================================================
# from src.clip_color_detector import ClipColorDetector
# from src.color_match_agent import ColorMatchAgent

# app = FastAPI(title="Product Color Detection API (GPT Only)")
# IMAGE_DIR = "data/images"

# # ==================================================
# # MIDDLEWARE
# # ==================================================
# @app.middleware("http")
# async def log_requests(request, call_next):
#     logger.info(f">>> {request.method} {request.url.path}")
#     response = await call_next(request)
#     logger.info(f"<<< {request.method} {request.url.path} | Status: {response.status_code}")
#     return response

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ==================================================
# # CONFIG
# # ==================================================
# OUTPUT_CSV_PATH = "data/hf_products_with_verdict.csv"
# COLOR_COLUMN_CANDIDATES = ["baseColour", "base_colour", "color", "colour"]
# NAME_COLUMN_CANDIDATES = ["productDisplayName", "product_name", "name", "title"]

# def sanitize_id(raw: str) -> str:
#     safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(raw))
#     return safe or "unknown"

# def get_image_path(product_id: str, index: Optional[int] = None) -> Optional[str]:
#     safe_id = sanitize_id(product_id)
#     if index is not None:
#         for ext in [".jpg", ".jpeg", ".png"]:
#             path = os.path.join(IMAGE_DIR, f"{index:05d}_{safe_id}{ext}")
#             if os.path.exists(path):
#                 return path
#         prefix = f"{index:05d}_"
#         if os.path.exists(IMAGE_DIR):
#             for fname in os.listdir(IMAGE_DIR):
#                 if fname.startswith(prefix) and fname.lower().endswith((".jpg", ".jpeg", ".png")):
#                     return os.path.join(IMAGE_DIR, fname)
#     if os.path.exists(IMAGE_DIR):
#         for fname in os.listdir(IMAGE_DIR):
#             if safe_id in fname and fname.lower().endswith((".jpg", ".jpeg", ".png")):
#                 return os.path.join(IMAGE_DIR, fname)
#     return None

# # ==================================================
# # COMPONENTS
# # ==================================================
# logger.info("Initializing ClipColorDetector...")
# detector = ClipColorDetector()

# logger.info("Initializing ColorMatchAgent...")
# agent = ColorMatchAgent(openai_api_key=os.getenv("OPENAI_API_KEY"))

# logger.info("FastAPI Color Detection Backend Started Successfully.")

# # ==================================================
# # ENDPOINTS
# # ==================================================
# @app.get("/")
# def home():
#     return {"message": "Server is running! Go to /docs to test the API."}

# @app.get("/health")
# def health():
#     logger.info("Health check requested.")
#     return {"status": "ok", "mode": "gpt-vision-only"}

# @app.get("/image/{product_id}")
# def get_product_image(product_id: str, index: Optional[int] = Query(None)):
#     logger.info(f"Image requested: product_id={product_id}, index={index}")
#     img_path = get_image_path(product_id, index)
#     if img_path is None or not os.path.exists(img_path):
#         logger.warning(f"Image not found for product_id={product_id}")
#         raise HTTPException(status_code=404, detail=f"Image not found for product ID: {product_id}")
#     ext = os.path.splitext(img_path)[1].lower()
#     media_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
#     return FileResponse(img_path, media_type=media_type)

# @app.get("/dataset")
# def get_dataset():
#     logger.info("Dataset fetch requested.")
#     if not os.path.exists(OUTPUT_CSV_PATH):
#         logger.error(f"CSV not found at: {OUTPUT_CSV_PATH}")
#         raise HTTPException(status_code=404, detail=f"Output CSV not found at: {OUTPUT_CSV_PATH}")

#     df = pd.read_csv(OUTPUT_CSV_PATH)
#     if df.empty:
#         logger.warning("Dataset CSV is empty.")
#         raise HTTPException(status_code=400, detail="Dataset is empty.")

#     color_col = next((c for c in COLOR_COLUMN_CANDIDATES if c in df.columns), None)
#     if color_col is None:
#         logger.error("No valid color column found in CSV.")
#         raise HTTPException(status_code=400, detail="Could not find a color column.")

#     name_col = next((c for c in NAME_COLUMN_CANDIDATES if c in df.columns), None)
#     records = df.where(pd.notnull(df), None).to_dict(orient="records")
#     logger.info(f"Returning {len(records)} dataset rows.")
#     return {"rows": records, "color_column": color_col, "name_column": name_col}

# @app.post("/detect-color")
# async def detect_color(
#     file: UploadFile = File(...),
#     top_k: int = Form(3),
#     confidence_threshold: float = Form(0.25),
# ):
#     logger.info(f"Detect color request: file={file.filename}, top_k={top_k}")
#     img_bytes = await file.read()
#     image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
#     result = detector.detect_color(
#         image=image,
#         candidate_colors=None,
#         top_k=top_k,
#         confidence_threshold=confidence_threshold,
#     )
#     logger.info(f"Detection result: {result}")
#     return result

# @app.post("/match-color")
# async def match_color(
#     expected_color: str = Form(...),
#     detected_color: str = Form(...),
# ):
#     logger.info(f"Match color: expected={expected_color}, detected={detected_color}")
#     verdict = agent.get_verdict(expected_color, detected_color)
#     logger.info(f"Verdict: {verdict}")
#     return {"expected_color": expected_color, "detected_color": detected_color, "verdict": verdict}

# @app.post("/detect-and-match")
# async def detect_and_match(
#     file: UploadFile = File(...),
#     expected_color: str = Form(...),
# ):
#     logger.info(f"Detect-and-match request: file={file.filename}, expected={expected_color}")
#     img_bytes = await file.read()
#     image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
#     det = detector.detect_color(image=image)
#     logger.info(f"Detected color: {det.get('detected_color')}")
#     verdict = agent.get_verdict(expected_color=expected_color, detected_color=det["detected_color"])
#     logger.info(f"Verdict: {verdict}")
#     return {"detection": det, "expected_color": expected_color, "verdict": verdict}

# if __name__ == "__main__":
#     uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8020, reload=True)


from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from PIL import Image
import io
import os
import re
import urllib.request
from typing import Optional
import uvicorn
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# ==================================================
# LOGGING — must be first, before other imports
# ==================================================
import logging
import sys

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
logger = logging.getLogger("ColorDetection-Backend")

# ==================================================
# APP IMPORTS (after logging)
# ==================================================
from ProductColorMismatch.src.clip_color_detector import ClipColorDetector
from ProductColorMismatch.src.color_match_agent import ColorMatchAgent

app = FastAPI(title="Product Color Detection API (GPT Only)")

# ==================================================
# AZURE BLOB STORAGE CONFIG
# Images are now served from Azure Blob Storage
# instead of local disk (data/images folder)
# ==================================================
AZURE_ACCOUNT   = "ecommerceblobvtryon"
AZURE_CONTAINER = "vtryon"
AZURE_FOLDER    = "Product_Colour_MisMatch"
BLOB_BASE_URL   = f"https://{AZURE_ACCOUNT}.blob.core.windows.net/{AZURE_CONTAINER}/{AZURE_FOLDER}"

# ==================================================
# MIDDLEWARE
# ==================================================
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f">>> {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"<<< {request.method} {request.url.path} | Status: {response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# CONFIG
# ==================================================
# OUTPUT_CSV_PATH = "data/hf_products_with_verdict.csv"
OUTPUT_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "hf_products_with_verdict.csv")
COLOR_COLUMN_CANDIDATES = ["baseColour", "base_colour", "color", "colour"]
NAME_COLUMN_CANDIDATES  = ["productDisplayName", "product_name", "name", "title"]


def sanitize_id(raw: str) -> str:
    """Sanitize product ID for blob filename matching."""
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(raw))
    return safe or "unknown"


def get_blob_image_url(product_id: str, index: Optional[int] = None) -> Optional[str]:
    """
    Build the Azure Blob URL for a product image.

    Blob naming pattern (confirmed from your blob list):
        {index:05d}_{product_id}.jpg   e.g.  00001_39386.jpg
        {index:05d}_{product_id}.png   e.g.  00001_39386.png  (some are .png)

    Logic:
    1. If index is provided → try {index:05d}_{product_id}.jpg then .png
    2. If not found / no index → HEAD-check .jpg then .png as fallback
    3. Returns the first URL that responds with HTTP 200
    4. Falls back to .jpg URL if nothing found (frontend shows broken image)
    """
    safe_id = sanitize_id(product_id)

    # Build candidate URLs in priority order
    candidates = []
    if index is not None:
        candidates += [
            f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.jpg",
            f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.png",
            f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.jpeg",
        ]
    # Also try without index prefix (in case product_id alone matches)
    candidates += [
        f"{BLOB_BASE_URL}/{safe_id}.jpg",
        f"{BLOB_BASE_URL}/{safe_id}.png",
        f"{BLOB_BASE_URL}/{safe_id}.jpeg",
    ]

    # HEAD-check each candidate URL
    for url in candidates:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    logger.info(f"Blob found: {url}")
                    return url
        except Exception:
            continue

    # Fallback — return the most likely URL even if not verified
    fallback = (
        f"{BLOB_BASE_URL}/{index:05d}_{safe_id}.jpg"
        if index is not None
        else f"{BLOB_BASE_URL}/{safe_id}.jpg"
    )
    logger.warning(f"Blob not found for product_id={product_id}, index={index}. Fallback: {fallback}")
    return fallback


# ==================================================
# COMPONENTS
# ==================================================
logger.info("Initializing ClipColorDetector...")
detector = ClipColorDetector()

logger.info("Initializing ColorMatchAgent...")
agent = ColorMatchAgent(openai_api_key=os.getenv("OPENAI_API_KEY"))

logger.info("FastAPI Color Detection Backend Started Successfully.")
logger.info(f"Images served from Azure Blob: {BLOB_BASE_URL}")

# ==================================================
# ENDPOINTS
# ==================================================
@app.get("/")
def home():
    return {"message": "Server is running! Go to /docs to test the API."}


@app.get("/health")
def health():
    logger.info("Health check requested.")
    return {"status": "ok", "mode": "gpt-vision-only"}


@app.get("/image/{product_id}")
def get_product_image(product_id: str, index: Optional[int] = Query(None)):
    """
    Returns the product image from Azure Blob Storage.
    Previously served from local disk — now redirects to Azure Blob URL.

    Usage:
        GET /image/39386          → tries to find blob with product_id=39386
        GET /image/39386?index=1  → looks for 00001_39386.jpg in blob
    """
    logger.info(f"Image requested: product_id={product_id}, index={index}")

    blob_url = get_blob_image_url(product_id, index)

    if blob_url is None:
        logger.warning(f"Image not found for product_id={product_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Image not found for product ID: {product_id}"
        )

    # Redirect browser directly to Azure Blob URL
    # This replaces the old FileResponse(local_path) call
    logger.info(f"Redirecting to blob URL: {blob_url}")
    return RedirectResponse(url=blob_url)


@app.get("/dataset")
def get_dataset():
    """Browse the processed dataset. Returns product records with image blob URLs."""
    logger.info("Dataset fetch requested.")

    if not os.path.exists(OUTPUT_CSV_PATH):
        logger.error(f"CSV not found at: {OUTPUT_CSV_PATH}")
        raise HTTPException(
            status_code=404,
            detail=f"Output CSV not found at: {OUTPUT_CSV_PATH}"
        )

    df = pd.read_csv(OUTPUT_CSV_PATH)
    if df.empty:
        logger.warning("Dataset CSV is empty.")
        raise HTTPException(status_code=400, detail="Dataset is empty.")

    color_col = next((c for c in COLOR_COLUMN_CANDIDATES if c in df.columns), None)
    if color_col is None:
        logger.error("No valid color column found in CSV.")
        raise HTTPException(status_code=400, detail="Could not find a color column.")

    name_col = next((c for c in NAME_COLUMN_CANDIDATES if c in df.columns), None)

    # Inject blob image URL into each record
    records = df.where(pd.notnull(df), None).to_dict(orient="records")
    for i, row in enumerate(records):
        product_id = str(row.get("id") or row.get("product_id") or i)
        row["image_url"] = get_blob_image_url(product_id, index=i)

    logger.info(f"Returning {len(records)} dataset rows.")
    return {
        "rows": records,
        "color_column": color_col,
        "name_column": name_col,
    }


@app.post("/detect-color")
async def detect_color(
    file: UploadFile = File(...),
    top_k: int = Form(3),
    confidence_threshold: float = Form(0.25),
):
    logger.info(f"Detect color request: file={file.filename}, top_k={top_k}")
    img_bytes = await file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    result = detector.detect_color(
        image=image,
        candidate_colors=None,
        top_k=top_k,
        confidence_threshold=confidence_threshold,
    )
    logger.info(f"Detection result: {result}")
    return result


@app.post("/match-color")
async def match_color(
    expected_color: str = Form(...),
    detected_color: str = Form(...),
):
    logger.info(f"Match color: expected={expected_color}, detected={detected_color}")
    verdict = agent.get_verdict(expected_color, detected_color)
    logger.info(f"Verdict: {verdict}")
    return {
        "expected_color": expected_color,
        "detected_color": detected_color,
        "verdict": verdict,
    }


@app.post("/detect-and-match")
async def detect_and_match(
    file: UploadFile = File(...),
    expected_color: str = Form(...),
):
    logger.info(f"Detect-and-match request: file={file.filename}, expected={expected_color}")
    img_bytes = await file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    det = detector.detect_color(image=image)
    logger.info(f"Detected color: {det.get('detected_color')}")
    verdict = agent.get_verdict(
        expected_color=expected_color,
        detected_color=det["detected_color"]
    )
    logger.info(f"Verdict: {verdict}")
    return {
        "detection": det,
        "expected_color": expected_color,
        "verdict": verdict,
    }


if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8020, reload=True)
# # import os
# # import io
# # import logging
# # import base64
# # import time
# # from typing import Optional
# # from fastapi import FastAPI, File, UploadFile, HTTPException, Form
# # from fastapi.responses import Response, JSONResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from PIL import Image
# # from dotenv import load_dotenv
# # from google import genai
# # from google.genai import types
# # import mapping as mp
# # from logger import get_logger, configure_logging

# # # ==================================================
# # # 1. INITIALIZATION & LOGGING
# # # ==================================================
# # load_dotenv()

# # configure_logging()
# # logger = get_logger("VTO-Backend")

# # API_KEY = os.getenv("GEMINI_API_KEY")
# # if not API_KEY:
# #     logger.critical("GEMINI_API_KEY is missing from environment variables!")
# #     raise RuntimeError("GEMINI_API_KEY not found.")

# # logger.info("Initializing Gemini Client...")
# # client = genai.Client(api_key=API_KEY)
# # app = FastAPI(title="Gemini 3 Virtual Try-On API")
# # @app.middleware("http")
# # async def log_requests(request, call_next):
# #     logger.info(f"{request.method} {request.url.path}")
# #     response = await call_next(request)
# #     return response
# # # Configure CORS to allow frontend requests
# # # For production, you may want to restrict allow_origins to specific domains
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # Allow all origins for development and Render deployment
# #     allow_credentials=False,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # logger.info("FastAPI Backend Started Successfully.")

# # def encode_image_to_base64(image_path):
# #     if not os.path.exists(image_path):
# #         logger.warning(f"Image not found for encoding: {image_path}")
# #         return None
# #     try:
# #         with open(image_path, "rb") as img_file:
# #             return base64.b64encode(img_file.read()).decode('utf-8')
# #     except Exception as e:
# #         logger.error(f"Failed to encode image {image_path}: {e}")
# #         return None

# # # ==================================================
# # # 2. ENDPOINT: GET OPTIONS
# # # ==================================================
# # @app.post("/get-garment-options")
# # async def get_garment_options(
# #     gender: str = Form(...),
# #     category: str = Form(...),
# #     current_brand: str = Form(...),
# #     current_size: str = Form(...),
# #     target_brand: str = Form(...)
# # ):
# #     logger.info(f"Request: Get Options | {gender} | {category} | {current_brand} {current_size} -> {target_brand}")

# #     # 1. Get Mapped Size
# #     final_size = mp.get_mapped_size_by_category(
# #         category=category,
# #         gender=gender,
# #         from_brand=current_brand,
# #         from_size=current_size,
# #         to_brand=target_brand
# #     )

# #     if not final_size:
# #         logger.error("Mapping failed: Size returned None")
# #         return JSONResponse(status_code=400, content={"error": "Size mapping not found"})

# #     logger.info(f"Mapped Size: {final_size}")

# #     # 2. Build Directory Path
# #     base_dir = f"assets/inventory/{target_brand.lower()}/{gender}/{category}"
# #     if not os.path.exists(base_dir):
# #         logger.error(f"Inventory Directory Missing: {base_dir}")
# #         return JSONResponse(status_code=404, content={"error": f"Inventory folder missing for {target_brand}"})

# #     # 3. Find SKUs
# #     found_garments = []
# #     gender_code = gender[0] 

# #     for index in [1, 2, 3]:
# #         sku_found = False
# #         for ext in [".jpeg", ".jpg", ".png"]:
# #             filename = f"{target_brand.lower()}-{gender_code}-{category}-{final_size}-{index}{ext}"
# #             full_path = os.path.join(base_dir, filename)

# #             if os.path.exists(full_path):
# #                 found_garments.append({
# #                     "sku_index": index,
# #                     "path": full_path,
# #                     "filename": filename,
# #                     "image_base64": encode_image_to_base64(full_path)
# #                 })
# #                 sku_found = True
# #                 logger.debug(f"Found SKU: {filename}")
# #                 break 
        
# #         if not sku_found:
# #              logger.debug(f"SKU {index} not found for pattern {filename}")

# #     if not found_garments:
# #         logger.warning(f"No garments found in {base_dir} for size {final_size}")
# #         return JSONResponse(status_code=404, content={"error": f"No garments found for size {final_size}"})

# #     logger.info(f"Returning {len(found_garments)} garment options.")
# #     return {
# #         "status": "success",
# #         "mapped_size": final_size,
# #         "garments": found_garments
# #     }

# # # ==================================================
# # # 2.5. ENDPOINT: GET SUPPORTED SIZES (New - for dynamic dropdown)
# # # ==================================================
# # @app.get("/get-supported-sizes")
# # async def get_supported_sizes(
# #     category: str,
# #     gender: str,
# #     brand: str
# # ):
# #     """Returns valid sizes for the dropdown based on category, gender, and brand."""
# #     logger.info(f"Request: Get Supported Sizes | {category} | {gender} | {brand}")
    
# #     try:
# #         sizes = mp.get_supported_sizes(category, gender, brand)
# #         logger.info(f"Returning {len(sizes)} supported sizes: {sizes}")
# #         return {
# #             "status": "success",
# #             "sizes": sizes
# #         }
# #     except KeyError as e:
# #         logger.warning(f"Invalid parameters for size lookup: {e}")
# #         return JSONResponse(
# #             status_code=400,
# #             content={"error": f"Invalid category/gender/brand combination: {str(e)}"}
# #         )

# # # ==================================================
# # # 3. ENDPOINT: GENERATE TRY-ON
# # # ==================================================
# # @app.post("/generate-tryon")
# # async def generate_tryon(
# #     garment_path: str = Form(...),
# #     gender: str = Form(...),
# #     category: str = Form(...),
# #     user_image: Optional[UploadFile] = File(None)
# # ):
# #     logger.info("Request: Generate Try-On Started.")
# #     logger.info(f"Selected Garment: {garment_path}")

# #     # --- Load User Image ---
# #     try:
# #         if user_image:
# #             logger.info(f"Using uploaded user image: {user_image.filename}")
# #             img_bytes = await user_image.read()
# #             user_img = Image.open(io.BytesIO(img_bytes))
# #         else:
# #             default_path = f"assets/default_models/model_{gender}.jpg"
# #             logger.info(f"Using default model image: {default_path}")
# #             if not os.path.exists(default_path):
# #                 logger.error("Default model file is missing!")
# #                 raise FileNotFoundError(f"Default model missing at {default_path}")
# #             user_img = Image.open(default_path)
# #     except Exception as e:
# #         logger.error(f"Error loading user image: {e}")
# #         raise HTTPException(status_code=400, detail=f"User Image Error: {str(e)}")

# #     # --- Load Garment Image ---
# #     if not os.path.exists(garment_path):
# #         logger.error(f"Garment file not found: {garment_path}")
# #         raise HTTPException(status_code=404, detail="Selected garment file missing")
# #     cloth_img = Image.open(garment_path)

# #     # --- Gemini Generation (Retry Logic) ---
# #     prompt = (
# #         f"Perform a realistic virtual try-on. "
# #         f"Dress the person in the first image with the {category} garment from the second image. "
# #         "Maintain pose, lighting, and background exactly."
# #     )

# #     max_retries = 3
# #     for attempt in range(max_retries):
# #         try:
# #             logger.info(f"Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
            
# #             response = client.models.generate_content(
# #                 model="gemini-3-pro-image-preview",
# #                 contents=[user_img, cloth_img, prompt],
# #                 config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
# #             )

# #             if response.candidates:
# #                 for part in response.candidates[0].content.parts:
# #                     if part.inline_data:
# #                         logger.info("Gemini Generation Successful.")
# #                         return Response(content=part.inline_data.data, media_type="image/png")
            
# #             logger.warning("Gemini returned response but no inline image data.")
# #             raise ValueError("No image data in Gemini response.")

# #         except Exception as e:
# #             error_str = str(e)
# #             if "503" in error_str or "overloaded" in error_str.lower() or "500" in error_str:
# #                 wait_time = (attempt + 1) * 3
# #                 logger.warning(f"Gemini Server Busy (503/500). Waiting {wait_time}s...")
# #                 time.sleep(wait_time)
# #             else:
# #                 logger.error(f"Non-retriable Gemini Error: {error_str}")
# #                 raise HTTPException(status_code=500, detail=f"AI Engine Error: {error_str}")

# #     logger.critical("All retry attempts failed.")
# #     raise HTTPException(status_code=503, detail="Server is currently overloaded. Please wait 1 minute and try again.")


# import os
# import io
# import logging
# import base64
# import time
# from typing import Optional
# from fastapi import FastAPI, File, UploadFile, HTTPException, Form
# from fastapi.responses import Response, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from PIL import Image
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# # ==================================================
# # 1. LOGGING — must be configured FIRST, before any other import
# # ==================================================
# from logger import get_logger, configure_logging
# configure_logging()  # Called immediately — before mapping, before uvicorn touches anything
# logger = get_logger("VTO-Backend")

# import mapping as mp  # Import AFTER logging is configured

# # ==================================================
# # 2. INITIALIZATION
# # ==================================================
# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")
# if not API_KEY:
#     logger.critical("GEMINI_API_KEY is missing from environment variables!")
#     raise RuntimeError("GEMINI_API_KEY not found.")

# logger.info("Initializing Gemini Client...")
# client = genai.Client(api_key=API_KEY)

# app = FastAPI(title="Gemini Virtual Try-On API")

# @app.middleware("http")
# async def log_requests(request, call_next):
#     logger.info(f">>> {request.method} {request.url.path}")
#     response = await call_next(request)
#     logger.info(f"<<< {request.method} {request.url.path} | Status: {response.status_code}")
#     return response

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# logger.info("FastAPI Backend Started Successfully.")


# def encode_image_to_base64(image_path):
#     if not os.path.exists(image_path):
#         logger.warning(f"Image not found for encoding: {image_path}")
#         return None
#     try:
#         with open(image_path, "rb") as img_file:
#             return base64.b64encode(img_file.read()).decode('utf-8')
#     except Exception as e:
#         logger.error(f"Failed to encode image {image_path}: {e}")
#         return None


# # ==================================================
# # 3. ENDPOINT: GET OPTIONS
# # ==================================================
# @app.post("/get-garment-options")
# async def get_garment_options(
#     gender: str = Form(...),
#     category: str = Form(...),
#     current_brand: str = Form(...),
#     current_size: str = Form(...),
#     target_brand: str = Form(...)
# ):
#     logger.info(f"Request: Get Options | {gender} | {category} | {current_brand} {current_size} -> {target_brand}")

#     final_size = mp.get_mapped_size_by_category(
#         category=category,
#         gender=gender,
#         from_brand=current_brand,
#         from_size=current_size,
#         to_brand=target_brand
#     )

#     if not final_size:
#         logger.error("Mapping failed: Size returned None")
#         return JSONResponse(status_code=400, content={"error": "Size mapping not found"})

#     logger.info(f"Mapped Size: {final_size}")

#     base_dir = f"assets/inventory/{target_brand.lower()}/{gender}/{category}"
#     if not os.path.exists(base_dir):
#         logger.error(f"Inventory Directory Missing: {base_dir}")
#         return JSONResponse(status_code=404, content={"error": f"Inventory folder missing for {target_brand}"})

#     found_garments = []
#     gender_code = gender[0]

#     for index in [1, 2, 3]:
#         sku_found = False
#         for ext in [".jpeg", ".jpg", ".png"]:
#             filename = f"{target_brand.lower()}-{gender_code}-{category}-{final_size}-{index}{ext}"
#             full_path = os.path.join(base_dir, filename)
#             if os.path.exists(full_path):
#                 found_garments.append({
#                     "sku_index": index,
#                     "path": full_path,
#                     "filename": filename,
#                     "image_base64": encode_image_to_base64(full_path)
#                 })
#                 sku_found = True
#                 logger.debug(f"Found SKU: {filename}")
#                 break
#         if not sku_found:
#             logger.debug(f"SKU {index} not found for size {final_size}")

#     if not found_garments:
#         logger.warning(f"No garments found in {base_dir} for size {final_size}")
#         return JSONResponse(status_code=404, content={"error": f"No garments found for size {final_size}"})

#     logger.info(f"Returning {len(found_garments)} garment options.")
#     return {
#         "status": "success",
#         "mapped_size": final_size,
#         "garments": found_garments
#     }


# # ==================================================
# # 4. ENDPOINT: GET SUPPORTED SIZES
# # ==================================================
# @app.get("/get-supported-sizes")
# async def get_supported_sizes(category: str, gender: str, brand: str):
#     logger.info(f"Request: Get Supported Sizes | {category} | {gender} | {brand}")
#     try:
#         sizes = mp.get_supported_sizes(category, gender, brand)
#         logger.info(f"Returning {len(sizes)} supported sizes: {sizes}")
#         return {"status": "success", "sizes": sizes}
#     except KeyError as e:
#         logger.warning(f"Invalid parameters for size lookup: {e}")
#         return JSONResponse(status_code=400, content={"error": f"Invalid combination: {str(e)}"})


# # ==================================================
# # 5. ENDPOINT: GENERATE TRY-ON
# # ==================================================
# @app.post("/generate-tryon")
# async def generate_tryon(
#     garment_path: str = Form(...),
#     gender: str = Form(...),
#     category: str = Form(...),
#     user_image: Optional[UploadFile] = File(None)
# ):
#     logger.info("Request: Generate Try-On Started.")
#     logger.info(f"Selected Garment: {garment_path}")

#     try:
#         if user_image:
#             logger.info(f"Using uploaded user image: {user_image.filename}")
#             img_bytes = await user_image.read()
#             user_img = Image.open(io.BytesIO(img_bytes))
#         else:
#             default_path = f"assets/default_models/model_{gender}.jpg"
#             logger.info(f"Using default model image: {default_path}")
#             if not os.path.exists(default_path):
#                 logger.error("Default model file is missing!")
#                 raise FileNotFoundError(f"Default model missing at {default_path}")
#             user_img = Image.open(default_path)
#     except Exception as e:
#         logger.error(f"Error loading user image: {e}")
#         raise HTTPException(status_code=400, detail=f"User Image Error: {str(e)}")

#     if not os.path.exists(garment_path):
#         logger.error(f"Garment file not found: {garment_path}")
#         raise HTTPException(status_code=404, detail="Selected garment file missing")
#     cloth_img = Image.open(garment_path)

#     prompt = (
#         f"Perform a realistic virtual try-on. "
#         f"Dress the person in the first image with the {category} garment from the second image. "
#         "Maintain pose, lighting, and background exactly."
#     )

#     max_retries = 3
#     for attempt in range(max_retries):
#         try:
#             logger.info(f"Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
#             response = client.models.generate_content(
#                 model="gemini-3-pro-image-preview",
#                 contents=[user_img, cloth_img, prompt],
#                 config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
#             )

#             if response.candidates:
#                 for part in response.candidates[0].content.parts:
#                     if part.inline_data:
#                         logger.info("Gemini Generation Successful.")
#                         return Response(content=part.inline_data.data, media_type="image/png")

#             logger.warning("Gemini returned response but no inline image data.")
#             raise ValueError("No image data in Gemini response.")

#         except Exception as e:
#             error_str = str(e)
#             if "503" in error_str or "overloaded" in error_str.lower() or "500" in error_str:
#                 wait_time = (attempt + 1) * 3
#                 logger.warning(f"Gemini Server Busy (503/500). Waiting {wait_time}s before retry...")
#                 time.sleep(wait_time)
#             else:
#                 logger.error(f"Non-retriable Gemini Error: {error_str}")
#                 raise HTTPException(status_code=500, detail=f"AI Engine Error: {error_str}")

#     logger.critical("All retry attempts exhausted.")

import os
import io
import logging
import base64
import time
import urllib.request
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==================================================
# 1. LOGGING — must be configured FIRST
# ==================================================
from logger import get_logger, configure_logging
configure_logging()
logger = get_logger("VTO-Backend")

import mapping as mp  # Import AFTER logging is configured

# ==================================================
# 2. AZURE BLOB STORAGE CONFIG
#
# Container : vtryon
# Structure inside blob:
#   vtryon/default_models/model_female.jpg
#   vtryon/default_models/model_male.jpg
#   vtryon/inventory/{brand}/{gender}/{category}/{brand}-{g}-{category}-{size}-{index}.jpg/.jpeg
#
# Confirmed from blob list — all brands: adidas, nike, zara
# ==================================================
AZURE_ACCOUNT      = "ecommerceblobvtryon"
AZURE_CONTAINER    = "vtryon"
AZURE_FOLDER       = "vtryon"

BLOB_BASE_URL      = f"https://{AZURE_ACCOUNT}.blob.core.windows.net/{AZURE_CONTAINER}/{AZURE_FOLDER}"
BLOB_INVENTORY_URL = f"{BLOB_BASE_URL}/inventory"
BLOB_MODELS_URL    = f"{BLOB_BASE_URL}/default_models"


def blob_exists(url: str) -> bool:
    """HEAD-check a blob URL. Returns True if HTTP 200."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def get_garment_blob_url(brand: str, gender: str, category: str, size: str, index: int) -> Optional[str]:
    """
    Build Azure Blob URL for a garment image.

    Confirmed naming pattern from blob list:
        {brand}-{gender_code}-{category}-{size}-{index}.jpeg/.jpg

    Edge cases found in blob list and handled:
        1. Mixed extensions — some files are .jpg, others .jpeg
           e.g. adidas-m-tshirts-44-1.jpg  vs  adidas-m-tshirts-44-2.jpeg
        2. Double extension — zara-m-shoes-42-2.jpg.jpeg  (treat as .jpg.jpeg)
        3. Missing index   — zara-m-shoes-44.jpg          (no -{index} suffix)

    Strategy: try all known extension variants in order.
    Returns first URL that exists (HTTP 200), or None.
    """
    gender_code = gender[0].lower()
    base_name   = f"{brand.lower()}-{gender_code}-{category}-{size}-{index}"
    no_idx_name = f"{brand.lower()}-{gender_code}-{category}-{size}"   # edge case: no index
    folder_path = f"{BLOB_INVENTORY_URL}/{brand.lower()}/{gender}/{category}"

    candidates = [
        f"{folder_path}/{base_name}.jpeg",      # most common
        f"{folder_path}/{base_name}.jpg",        # also common
        f"{folder_path}/{base_name}.jpg.jpeg",   # edge case: zara shoes double ext
        f"{folder_path}/{base_name}.png",        # rare
        f"{folder_path}/{no_idx_name}.jpg",      # edge case: no index suffix
        f"{folder_path}/{no_idx_name}.jpeg",
    ]

    for url in candidates:
        if blob_exists(url):
            logger.debug(f"Garment blob found: {url}")
            return url

    logger.warning(f"No garment blob found for {base_name} in {folder_path}")
    return None


def get_model_blob_url(gender: str) -> Optional[str]:
    """
    Build Azure Blob URL for the default model image.

    Confirmed from blob list:
        vtryon/default_models/model_female.jpg
        vtryon/default_models/model_male.jpg
    """
    for ext in ["jpg", "jpeg", "png"]:
        url = f"{BLOB_MODELS_URL}/model_{gender}.{ext}"
        if blob_exists(url):
            logger.debug(f"Model blob found: {url}")
            return url

    logger.warning(f"No default model blob found for gender={gender}")
    return None


def load_image_from_blob(url: str) -> Image.Image:
    """Download a blob image from URL and return as PIL Image."""
    with urllib.request.urlopen(url, timeout=10) as resp:
        return Image.open(io.BytesIO(resp.read()))


def encode_blob_image_to_base64(url: str) -> Optional[str]:
    """Download blob image from URL and return base64 string."""
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return base64.b64encode(resp.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Failed to encode blob image {url}: {e}")
        return None


# ==================================================
# 3. INITIALIZATION
# ==================================================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.critical("GEMINI_API_KEY is missing from environment variables!")
    raise RuntimeError("GEMINI_API_KEY not found.")

logger.info("Initializing Gemini Client...")
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="Gemini Virtual Try-On API")

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f">>> {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"<<< {request.method} {request.url.path} | Status: {response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("FastAPI VTO Backend Started Successfully.")
logger.info(f"Assets served from Azure Blob: {BLOB_BASE_URL}")


# ==================================================
# 4. ENDPOINT: GET GARMENT OPTIONS
# ==================================================
@app.post("/get-garment-options")
async def get_garment_options(
    gender: str        = Form(...),
    category: str      = Form(...),
    current_brand: str = Form(...),
    current_size: str  = Form(...),
    target_brand: str  = Form(...)
):
    logger.info(
        f"Request: Get Options | {gender} | {category} | "
        f"{current_brand} {current_size} -> {target_brand}"
    )

    # Size mapping — logic unchanged
    final_size = mp.get_mapped_size_by_category(
        category=category,
        gender=gender,
        from_brand=current_brand,
        from_size=current_size,
        to_brand=target_brand
    )

    if not final_size:
        logger.error("Mapping failed: Size returned None")
        return JSONResponse(status_code=400, content={"error": "Size mapping not found"})

    logger.info(f"Mapped Size: {final_size}")

    # Find garments from Azure Blob instead of local disk
    found_garments = []

    for index in [1, 2, 3]:
        blob_url = get_garment_blob_url(
            brand=target_brand,
            gender=gender,
            category=category,
            size=final_size,
            index=index
        )

        if blob_url:
            found_garments.append({
                "sku_index":    index,
                "path":         blob_url,                           # blob URL used by /generate-tryon
                "filename":     blob_url.split("/")[-1],
                "image_base64": encode_blob_image_to_base64(blob_url)
            })
            logger.debug(f"Found SKU {index}: {blob_url}")
        else:
            logger.debug(f"SKU {index} not found for size={final_size}")

    if not found_garments:
        logger.warning(
            f"No garments found in blob: "
            f"{target_brand}/{gender}/{category} size={final_size}"
        )
        return JSONResponse(
            status_code=404,
            content={"error": f"No garments found for size {final_size}"}
        )

    logger.info(f"Returning {len(found_garments)} garment options.")
    return {
        "status":      "success",
        "mapped_size": final_size,
        "garments":    found_garments
    }


# ==================================================
# 5. ENDPOINT: GET SUPPORTED SIZES
# ==================================================
@app.get("/get-supported-sizes")
async def get_supported_sizes(category: str, gender: str, brand: str):
    logger.info(f"Request: Get Supported Sizes | {category} | {gender} | {brand}")
    try:
        sizes = mp.get_supported_sizes(category, gender, brand)
        logger.info(f"Returning {len(sizes)} supported sizes: {sizes}")
        return {"status": "success", "sizes": sizes}
    except KeyError as e:
        logger.warning(f"Invalid parameters for size lookup: {e}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid combination: {str(e)}"}
        )


# ==================================================
# 6. ENDPOINT: GENERATE TRY-ON
# ==================================================
@app.post("/generate-tryon")
async def generate_tryon(
    garment_path: str                = Form(...),   # blob URL from /get-garment-options
    gender: str                      = Form(...),
    category: str                    = Form(...),
    user_image: Optional[UploadFile] = File(None)
):
    logger.info("Request: Generate Try-On Started.")
    logger.info(f"Selected Garment: {garment_path}")

    # ── Load user image ──────────────────────────────────────────
    try:
        if user_image:
            logger.info(f"Using uploaded user image: {user_image.filename}")
            img_bytes = await user_image.read()
            user_img  = Image.open(io.BytesIO(img_bytes))
        else:
            # Load default model from Azure Blob
            model_url = get_model_blob_url(gender)
            if not model_url:
                logger.error(f"Default model blob missing for gender={gender}")
                raise FileNotFoundError(
                    f"Default model not found in blob. "
                    f"Expected: {BLOB_MODELS_URL}/model_{gender}.jpg"
                )
            logger.info(f"Loading default model from blob: {model_url}")
            user_img = load_image_from_blob(model_url)

    except Exception as e:
        logger.error(f"Error loading user image: {e}")
        raise HTTPException(status_code=400, detail=f"User Image Error: {str(e)}")

    # ── Load garment image ───────────────────────────────────────
    try:
        if garment_path.startswith("http"):
            # Load from Azure Blob URL
            logger.info(f"Loading garment from blob: {garment_path}")
            cloth_img = load_image_from_blob(garment_path)
        else:
            # Fallback: still support old local paths if passed
            if not os.path.exists(garment_path):
                logger.error(f"Garment not found locally: {garment_path}")
                raise HTTPException(status_code=404, detail="Garment file missing")
            cloth_img = Image.open(garment_path)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading garment: {e}")
        raise HTTPException(status_code=400, detail=f"Garment load error: {str(e)}")

    # ── Call Gemini API ──────────────────────────────────────────
    prompt = (
        f"Perform a realistic virtual try-on. "
        f"Dress the person in the first image with the {category} garment from the second image. "
        "Maintain pose, lighting, and background exactly."
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[user_img, cloth_img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                )
            )

            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        logger.info("Gemini Generation Successful.")
                        return Response(
                            content=part.inline_data.data,
                            media_type="image/png"
                        )

            logger.warning("Gemini returned no inline image data.")
            raise ValueError("No image data in Gemini response.")

        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "overloaded" in error_str.lower() or "500" in error_str:
                wait_time = (attempt + 1) * 3
                logger.warning(f"Gemini busy. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Non-retriable Gemini Error: {error_str}")
                raise HTTPException(status_code=500, detail=f"AI Engine Error: {error_str}")

    logger.critical("All retry attempts exhausted.")
    raise HTTPException(
        status_code=503,
        detail="Server is currently overloaded. Please wait 1 minute and try again."
    )
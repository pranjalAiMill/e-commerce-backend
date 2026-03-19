# import os
# import io
# import logging
# import time
# import base64
# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.responses import JSONResponse, StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# import json
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# from PIL import Image

# # Import the database function
# from backend.data import get_template_database

# # ==================================================
# # 1. SETUP
# # ==================================================
# load_dotenv()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - Backend - %(levelname)s - %(message)s')
# logger = logging.getLogger("Backend") 

# API_KEY = os.getenv("GEMINI_API_KEY")
# if not API_KEY:
#     raise RuntimeError("GEMINI_API_KEY not found in .env file!")

# logger.info("Initializing Gemini Client...")
# client = genai.Client(api_key=API_KEY)

# app = FastAPI(title="AI Photoshoot Generator")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Robust Asset Mounting
# CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(CURRENT_FILE_DIR)
# ASSETS_PATH = os.path.join(PROJECT_ROOT, "assets")

# if os.path.exists(ASSETS_PATH):
#     app.mount("/static", StaticFiles(directory=ASSETS_PATH), name="static")
# else:
#     logger.error(f"❌ Assets folder missing at: {ASSETS_PATH}")

# # ==================================================
# # 2. GENERATION LOGIC (IDENTITY PRESERVATION)
# # ==================================================

# def generate_view(cloth_image, reference_person_image, base_prompt, view_name, skin_tone):
#     """
#     Generates a specific view. 
#     If 'reference_person_image' is provided, it uses it to maintain consistency.
#     """
    
#     # 1. Prepare Inputs
#     # If we have a reference person (from Front view), we send BOTH images.
#     input_content = [cloth_image]
    
#     identity_instruction = ""
#     if reference_person_image:
#         input_content.append(reference_person_image)
#         identity_instruction = (
#             "CRITICAL REQUIREMENT: Use the SECOND image (the person) as the EXACT reference for the model's identity. "
#             "Keep the SAME face, SAME hairstyle, SAME body shape, and SAME skin tone. "
#             "Only change the pose to the requested view. "
#         )

#     # 2. Define View-Specific Prompts
#     view_instruction = ""
#     if view_name == "Front":
#         view_instruction = "Full body Front facing view. Looking at camera. Symmetrical."
#     elif view_name == "Side":
#         view_instruction = "Side profile view (90 degrees). Show the side details of the outfit. Keep the same model identity."
#     elif view_name == "Angle":
#         view_instruction = "3/4th Angle dynamic pose. Show movement and depth. Keep the same model identity. Pose Distinctly different from the Front and Side views."

#     # 3. Construct Final Prompt
#     final_prompt = (
#         f"Virtual Photoshoot Task. "
#         f"Dress the model in the clothing provided in the first image. "
#         f"{identity_instruction}"
#         f"Model Details: Photorealistic, {skin_tone} skin tone. "
#         f"Setting: {base_prompt} "
#         f"Viewpoint: {view_instruction} "
#         f"Output: High fidelity, consistent character, photorealistic 4k."
#     )

#     # 4. Call API
#     try:
#         response = client.models.generate_content(
#             model="gemini-3-pro-image-preview",
#             contents=[*input_content, final_prompt], # Unpack inputs + prompt
#             config=types.GenerateContentConfig(response_modalities=["IMAGE"])
#         )
#         if response.candidates:
#             for part in response.candidates[0].content.parts:
#                 if part.inline_data:
#                     # Return Base64 String AND the PIL Image (for next step)
#                     b64_data = base64.b64encode(part.inline_data.data).decode('utf-8')
#                     img_obj = Image.open(io.BytesIO(part.inline_data.data))
#                     return b64_data, img_obj
#     except Exception as e:
#         logger.error(f"Error generating {view_name}: {e}")
#         return None, None
#     return None, None

# # ==================================================
# # 3. ENDPOINTS
# # ==================================================

# @app.get("/templates")
# def get_templates():
#     return get_template_database()

# async def generate_photoshoot_stream(
#     template_id: str,
#     region: str,
#     skin_tone: str,
#     cloth_part: Image.Image,
#     selected_template: dict
# ):
#     """Generator function that yields images as they're generated"""
#     # --- STEP 1: Generate FRONT View (The Master Reference) ---
#     logger.info("Generating View 1: Front (Master)...")
#     front_b64, front_img_obj = generate_view(
#         cloth_image=cloth_part,
#         reference_person_image=None, # No reference for the first one
#         base_prompt=selected_template['prompt'],
#         view_name="Front",
#         skin_tone=skin_tone
#     )
    
#     if not front_b64:
#         yield f"data: {json.dumps({'status': 'error', 'message': 'Failed to generate primary Front view.'})}\n\n"
#         return
    
#     # Send Front view immediately
#     yield f"data: {json.dumps({'status': 'progress', 'view': 'Front', 'image': front_b64})}\n\n"

#     # --- STEP 2: Generate SIDE View (Using Front as Reference) ---
#     logger.info("Generating View 2: Side (Consistent)...")
#     side_b64, _ = generate_view(
#         cloth_image=cloth_part,
#         reference_person_image=front_img_obj, # <--- PASSING THE GENERATED MODEL
#         base_prompt=selected_template['prompt'],
#         view_name="Side",
#         skin_tone=skin_tone
#     )
#     if side_b64:
#         yield f"data: {json.dumps({'status': 'progress', 'view': 'Side', 'image': side_b64})}\n\n"

#     # --- STEP 3: Generate ANGLE View (Using Front as Reference) ---
#     logger.info("Generating View 3: Angle (Consistent)...")
#     angle_b64, _ = generate_view(
#         cloth_image=cloth_part,
#         reference_person_image=front_img_obj, # <--- PASSING THE GENERATED MODEL
#         base_prompt=selected_template['prompt'],
#         view_name="Angle",
#         skin_tone=skin_tone
#     )
#     if angle_b64:
#         yield f"data: {json.dumps({'status': 'progress', 'view': 'Angle', 'image': angle_b64})}\n\n"
    
#     # Send completion signal
#     yield f"data: {json.dumps({'status': 'completed'})}\n\n"

# @app.post("/generate-photoshoot")
# async def generate_photoshoot(
#     template_id: str = Form(...),
#     region: str = Form(...),
#     skin_tone: str = Form(...),
#     cloth_image: UploadFile = File(...),
#     stream: str = Form("false")  # New parameter for streaming (as string)
# ):
#     # Convert string to boolean
#     use_stream = stream.lower() == "true"
#     logger.info(f"Request: {region} | {template_id} (Consistency Mode) | Stream: {use_stream}")

#     # 1. Get Data
#     db = get_template_database()
#     selected_template = next((t for t in db.get(region, []) if t["id"] == template_id), None)
#     if not selected_template:
#         all_templates = [t for cat in db.values() for t in cat]
#         selected_template = next((t for t in all_templates if t["id"] == template_id), None)
    
#     if not selected_template:
#         raise HTTPException(status_code=404, detail="Template ID not found")

#     # 2. Load Cloth Image
#     try:
#         content = await cloth_image.read()
#         cloth_part = Image.open(io.BytesIO(content))
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Invalid image file")

#     # If streaming is requested, use Server-Sent Events
#     if use_stream:
#         return StreamingResponse(
#             generate_photoshoot_stream(template_id, region, skin_tone, cloth_part, selected_template),
#             media_type="text/event-stream",
#             headers={
#                 "Cache-Control": "no-cache",
#                 "Connection": "keep-alive",
#                 "X-Accel-Buffering": "no"  # Disable buffering for nginx
#             }
#         )

#     # Original non-streaming behavior (for backward compatibility)
#     generated_results = []
    
#     # --- STEP 1: Generate FRONT View (The Master Reference) ---
#     logger.info("Generating View 1: Front (Master)...")
#     front_b64, front_img_obj = generate_view(
#         cloth_image=cloth_part,
#         reference_person_image=None, # No reference for the first one
#         base_prompt=selected_template['prompt'],
#         view_name="Front",
#         skin_tone=skin_tone
#     )
    
#     if not front_b64:
#         raise HTTPException(status_code=500, detail="Failed to generate primary Front view.")
    
#     generated_results.append({"view": "Front", "image": front_b64})

#     # --- STEP 2: Generate SIDE View (Using Front as Reference) ---
#     logger.info("Generating View 2: Side (Consistent)...")
#     side_b64, _ = generate_view(
#         cloth_image=cloth_part,
#         reference_person_image=front_img_obj, # <--- PASSING THE GENERATED MODEL
#         base_prompt=selected_template['prompt'],
#         view_name="Side",
#         skin_tone=skin_tone
#     )
#     if side_b64:
#         generated_results.append({"view": "Side", "image": side_b64})

#     # --- STEP 3: Generate ANGLE View (Using Front as Reference) ---
#     logger.info("Generating View 3: Angle (Consistent)...")
#     angle_b64, _ = generate_view(
#         cloth_image=cloth_part,
#         reference_person_image=front_img_obj, # <--- PASSING THE GENERATED MODEL
#         base_prompt=selected_template['prompt'],
#         view_name="Angle",
#         skin_tone=skin_tone
#     )
#     if angle_b64:
#         generated_results.append({"view": "Angle", "image": angle_b64})

#     return JSONResponse(content={"status": "success", "images": generated_results})

import os
import io
import logging
import sys
import time
import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# ==================================================
# 1. LOGGING — before everything else
# ==================================================
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
logger = logging.getLogger("Photoshoot-Backend")

# ==================================================
# 2. SETUP
# ==================================================
load_dotenv()

from backend.data import get_template_database

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file!")

logger.info("Initializing Gemini Client...")
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="AI Photoshoot Generator")

# ==================================================
# 3. MIDDLEWARE
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust Asset Mounting
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_FILE_DIR)
ASSETS_PATH = os.path.join(PROJECT_ROOT, "assets")

if os.path.exists(ASSETS_PATH):
    app.mount("/static", StaticFiles(directory=ASSETS_PATH), name="static")
    logger.info(f"Assets mounted at: {ASSETS_PATH}")
else:
    logger.error(f"Assets folder missing at: {ASSETS_PATH}")

logger.info("FastAPI Photoshoot Backend Started Successfully.")

# ==================================================
# 4. GENERATION LOGIC
# ==================================================
def generate_view(cloth_image, reference_person_image, base_prompt, view_name, skin_tone):
    input_content = [cloth_image]
    identity_instruction = ""
    if reference_person_image:
        input_content.append(reference_person_image)
        identity_instruction = (
            "CRITICAL REQUIREMENT: Use the SECOND image (the person) as the EXACT reference for the model's identity. "
            "Keep the SAME face, SAME hairstyle, SAME body shape, and SAME skin tone. "
            "Only change the pose to the requested view. "
        )

    view_instruction = ""
    if view_name == "Front":
        view_instruction = "Full body Front facing view. Looking at camera. Symmetrical."
    elif view_name == "Side":
        view_instruction = "Side profile view (90 degrees). Show the side details of the outfit. Keep the same model identity."
    elif view_name == "Angle":
        view_instruction = "3/4th Angle dynamic pose. Show movement and depth. Keep the same model identity. Pose Distinctly different from the Front and Side views."

    final_prompt = (
        f"Virtual Photoshoot Task. "
        f"Dress the model in the clothing provided in the first image. "
        f"{identity_instruction}"
        f"Model Details: Photorealistic, {skin_tone} skin tone. "
        f"Setting: {base_prompt} "
        f"Viewpoint: {view_instruction} "
        f"Output: High fidelity, consistent character, photorealistic 4k."
    )

    try:
        logger.info(f"Calling Gemini API for view: {view_name}...")
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[*input_content, final_prompt],
            config=types.GenerateContentConfig(response_modalities=["IMAGE"])
        )
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    logger.info(f"View '{view_name}' generated successfully.")
                    b64_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                    img_obj = Image.open(io.BytesIO(part.inline_data.data))
                    return b64_data, img_obj
    except Exception as e:
        logger.error(f"Error generating {view_name}: {e}")
        return None, None
    return None, None

# ==================================================
# 5. ENDPOINTS
# ==================================================
@app.get("/templates")
def get_templates():
    logger.info("Templates requested.")
    return get_template_database()

async def generate_photoshoot_stream(template_id, region, skin_tone, cloth_part, selected_template):
    logger.info("Generating View 1: Front (Master)...")
    front_b64, front_img_obj = generate_view(
        cloth_image=cloth_part,
        reference_person_image=None,
        base_prompt=selected_template['prompt'],
        view_name="Front",
        skin_tone=skin_tone
    )
    if not front_b64:
        yield f"data: {json.dumps({'status': 'error', 'message': 'Failed to generate primary Front view.'})}\n\n"
        return
    yield f"data: {json.dumps({'status': 'progress', 'view': 'Front', 'image': front_b64})}\n\n"

    logger.info("Generating View 2: Side (Consistent)...")
    side_b64, _ = generate_view(
        cloth_image=cloth_part,
        reference_person_image=front_img_obj,
        base_prompt=selected_template['prompt'],
        view_name="Side",
        skin_tone=skin_tone
    )
    if side_b64:
        yield f"data: {json.dumps({'status': 'progress', 'view': 'Side', 'image': side_b64})}\n\n"

    logger.info("Generating View 3: Angle (Consistent)...")
    angle_b64, _ = generate_view(
        cloth_image=cloth_part,
        reference_person_image=front_img_obj,
        base_prompt=selected_template['prompt'],
        view_name="Angle",
        skin_tone=skin_tone
    )
    if angle_b64:
        yield f"data: {json.dumps({'status': 'progress', 'view': 'Angle', 'image': angle_b64})}\n\n"

    yield f"data: {json.dumps({'status': 'completed'})}\n\n"

@app.post("/generate-photoshoot")
async def generate_photoshoot(
    template_id: str = Form(...),
    region: str = Form(...),
    skin_tone: str = Form(...),
    cloth_image: UploadFile = File(...),
    stream: str = Form("false")
):
    use_stream = stream.lower() == "true"
    logger.info(f"Request: region={region} | template={template_id} | skin_tone={skin_tone} | stream={use_stream}")

    db = get_template_database()
    selected_template = next((t for t in db.get(region, []) if t["id"] == template_id), None)
    if not selected_template:
        all_templates = [t for cat in db.values() for t in cat]
        selected_template = next((t for t in all_templates if t["id"] == template_id), None)
    if not selected_template:
        logger.error(f"Template not found: {template_id}")
        raise HTTPException(status_code=404, detail="Template ID not found")

    try:
        content = await cloth_image.read()
        cloth_part = Image.open(io.BytesIO(content))
        logger.info(f"Cloth image loaded: {cloth_image.filename}")
    except Exception as e:
        logger.error(f"Invalid image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image file")

    if use_stream:
        return StreamingResponse(
            generate_photoshoot_stream(template_id, region, skin_tone, cloth_part, selected_template),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"}
        )

    generated_results = []

    logger.info("Generating View 1: Front (Master)...")
    front_b64, front_img_obj = generate_view(
        cloth_image=cloth_part, reference_person_image=None,
        base_prompt=selected_template['prompt'], view_name="Front", skin_tone=skin_tone
    )
    if not front_b64:
        raise HTTPException(status_code=500, detail="Failed to generate primary Front view.")
    generated_results.append({"view": "Front", "image": front_b64})

    logger.info("Generating View 2: Side (Consistent)...")
    side_b64, _ = generate_view(
        cloth_image=cloth_part, reference_person_image=front_img_obj,
        base_prompt=selected_template['prompt'], view_name="Side", skin_tone=skin_tone
    )
    if side_b64:
        generated_results.append({"view": "Side", "image": side_b64})

    logger.info("Generating View 3: Angle (Consistent)...")
    angle_b64, _ = generate_view(
        cloth_image=cloth_part, reference_person_image=front_img_obj,
        base_prompt=selected_template['prompt'], view_name="Angle", skin_tone=skin_tone
    )
    if angle_b64:
        generated_results.append({"view": "Angle", "image": angle_b64})

    logger.info(f"Photoshoot complete. Generated {len(generated_results)} views.")
    return JSONResponse(content={"status": "success", "images": generated_results})
import json
import time
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

from app.logger import get_logger

log = get_logger(__name__)
MODEL_ID = "openbmb/MiniCPM-V-2_6"

_model_cache = None
_tokenizer_cache = None
_device = None


def _select_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_backend():
    """
    Load model once and cache it for reuse.
    This is a HUGE performance improvement - model loading takes 10-30 seconds!
    """
    global _model_cache, _tokenizer_cache, _device
    
    if _model_cache is not None and _tokenizer_cache is not None:
        log.info("vision_minicpm | load_backend | cache_hit | reusing model")
        return _model_cache, _tokenizer_cache

    if _device is None:
        _device = _select_device()
        log.info("vision_minicpm | load_backend | device=%s", _device)

    log.info("vision_minicpm | load_backend | loading model | model_id=%s (once, ~10-30s)", MODEL_ID)
    t0 = time.perf_counter()
    _tokenizer_cache = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True
    )

    _model_cache = AutoModel.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        torch_dtype=torch.float16 if _device.type != "cpu" else torch.float32
    ).to(_device).eval()

    elapsed = time.perf_counter() - t0
    log.info("vision_minicpm | load_backend | model loaded | device=%s elapsed_sec=%.2f", _device, elapsed)
    return _model_cache, _tokenizer_cache


def describe_image_json_minicpm(image_path: str, language: str):
    """
    Generate description using cached model (much faster after first load)
    """
    log.info("vision_minicpm | describe_image_json_minicpm | start | path=%s language=%s", image_path, language)
    t0 = time.perf_counter()
    model, tokenizer = load_backend()
    image = None
    try:
        image = Image.open(image_path).convert("RGB")

        # ---- instruction ----
        prompt = f"""
Look at the image and output ONLY valid JSON in {language}.

JSON schema:
{{
 "title": string,
 "short_description": string,
 "long_description": string,
 "bullet_points": [string],
 "attributes": {{
   "color": string,
   "material": string,
   "pattern": string,
   "category": string,
   "gender": string
 }}
}}

Rules:
- Only describe visible information
- No brand hallucination
- No extra text, ONLY JSON
"""

        # -------- MiniCPM expected format --------
        msgs = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        # ---- NOTE: image must be passed as separate argument ----
        with torch.no_grad():
            output = model.chat(
                image=image,
                msgs=msgs,
                tokenizer=tokenizer,
                device=_device,
                max_new_tokens=500,  # Reduced from 600 to 500 for faster generation
                do_sample=False
            )

        # ---- JSON extraction ----
        start = output.find("{")
        end = output.rfind("}")

        if start == -1 or end == -1:
            log.warning("vision_minicpm | describe_image_json_minicpm | no_json | path=%s", image_path)
            raise ValueError("MiniCPM did not return JSON:\n" + output)

        json_text = output[start:end+1]
        elapsed = time.perf_counter() - t0
        log.info("vision_minicpm | describe_image_json_minicpm | success | path=%s language=%s elapsed_sec=%.2f", image_path, language, elapsed)
        return json.loads(json_text)
    except Exception as e:
        elapsed = time.perf_counter() - t0
        log.error("vision_minicpm | describe_image_json_minicpm | failed | path=%s language=%s elapsed_sec=%.2f error=%s", 
                 image_path, language, elapsed, e)
        raise
    finally:
        # Ensure image is closed to prevent resource leaks
        if image is not None:
            image.close()

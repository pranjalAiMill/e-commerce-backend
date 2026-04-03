import base64
import os
import json
import time
from io import BytesIO
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

from app.logger import get_logger

load_dotenv()
log = get_logger(__name__)

# Create OpenAI client with timeout to prevent hanging
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    timeout=60.0,  # 60 second timeout for API calls
    max_retries=2  # Retry up to 2 times on transient failures
)


def _encode_image_b64_uri(image_path: str, max_size: int = 768) -> str:
    """
    Encode image to base64, with optional resizing for large images.
    Reduced max_size from 1024 to 768 for faster processing.
    """
    img = None
    try:
        img = Image.open(image_path).convert("RGB")
        
        # Resize if image is too large (reduces encoding time and API payload size)
        original_size = (img.width, img.height)
        if max(img.width, img.height) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            log.info("openai_vision | _encode_image_b64_uri | resized | path=%s original=%dx%d max_size=%d", 
                    image_path, original_size[0], original_size[1], max_size)

        # Use context manager for BytesIO to ensure cleanup
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=80, optimize=True)  # Reduced quality from 85 to 80 for smaller files
        img_bytes = buffer.getvalue()
        buffer.close()
        
        # Encode to base64
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"
    finally:
        # Ensure image is closed to prevent resource leaks
        if img is not None:
            img.close()


def describe_image_json_gpt4o(image_path: str, language: str):
    """
    GPT-4o Vision backend — cloud model
    Full JSON guaranteed using response_format=json_object
    Optimized for speed: reduced max_tokens, added timeout/retries
    """
    log.info("openai_vision | describe_image_json_gpt4o | start | path=%s language=%s", image_path, language)
    t0 = time.perf_counter()
    
    try:
        image_data_url = _encode_image_b64_uri(image_path)
        encode_time = time.perf_counter() - t0
        log.info("openai_vision | describe_image_json_gpt4o | encoded | path=%s encode_sec=%.2f", image_path, encode_time)

        api_t0 = time.perf_counter()
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a product content generation system. "
                        "You MUST return ONLY valid JSON. Be concise."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"Generate structured product content in {language} "
                                "for the image. Use only visible evidence. "
                                "Return exactly this JSON structure:\n"
                                "{\n"
                                '  \"title\": string,\n'
                                '  \"short_description\": string,\n'
                                '  \"long_description\": string,\n'
                                '  \"bullet_points\": [string],\n'
                                '  \"attributes\": {\n'
                                '    \"color\": string,\n'
                                '    \"material\": string,\n'
                                '    \"pattern\": string,\n'
                                '    \"category\": string,\n'
                                '    \"gender\": string\n'
                                "  }\n"
                                "}"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_url},
                        },
                    ],
                },
            ],
            max_tokens=500,  # Reduced from 700 to 500 for faster responses
            temperature=0.3,  # Lower temperature for faster, more deterministic output
        )

        api_elapsed = time.perf_counter() - api_t0
        elapsed = time.perf_counter() - t0
        log.info("openai_vision | describe_image_json_gpt4o | success | path=%s language=%s api_sec=%.2f total_sec=%.2f", 
                image_path, language, api_elapsed, elapsed)
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        elapsed = time.perf_counter() - t0
        log.error("openai_vision | describe_image_json_gpt4o | failed | path=%s language=%s elapsed_sec=%.2f error=%s", 
                 image_path, language, elapsed, e)
        raise

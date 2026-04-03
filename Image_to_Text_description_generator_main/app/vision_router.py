import os

from app.openai_vision import describe_image_json_gpt4o
from app.logger import get_logger

log = get_logger(__name__)


def describe_image_json(image_path: str, language: str):
    """
    Vision backend switcher.

    Backends:
        - gpt4o    (default)
        - minicpm
    """
    provider = os.environ.get("VISION_BACKEND", "gpt4o").lower()
    log.info("vision_router | describe_image_json | provider=%s image_path=%s language=%s", provider, image_path, language)

    if provider == "minicpm":
        from app.vision_minicpm import describe_image_json_minicpm  # lazy — only if needed
        return describe_image_json_minicpm(image_path, language)

    return describe_image_json_gpt4o(image_path, language)
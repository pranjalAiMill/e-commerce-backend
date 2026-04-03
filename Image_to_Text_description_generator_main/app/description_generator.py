from app.vision_router import describe_image_json
from app.logger import get_logger

log = get_logger(__name__)


def generate_description(image_path: str, language_code: str):
    """
    Unified entry point.
    Dispatches either GPT-4o or MiniCPM backend
    depending on environment variable or UI selection.
    """
    log.info("generate_description | image_path=%s language=%s", image_path, language_code)
    out = describe_image_json(
        image_path=image_path,
        language=language_code
    )
    log.info("generate_description | done | image_path=%s language=%s", image_path, language_code)
    return out

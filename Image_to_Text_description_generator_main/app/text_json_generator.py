
import torch
import json
import re
from app.text_model_loader import TextModelLoader
from app.text_prompt_builder import build_json_prompt

def _normalize_json_like(text: str) -> str:
    text = re.sub(r'(\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*):', r'\1"\2":', text)
    text = re.sub(r':\s*([^",\}\]]+)(\s*[\},])', r': "\1"\2', text)
    return text

def generate_json(description_text: str, language: str):
    model, tokenizer = TextModelLoader.load_model()
    prompt = build_json_prompt(description_text, language)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    match = re.search(r"\{.*\}", decoded, re.DOTALL)
    if not match:
        return {
            "status": "FAILED",
            "reason": "NO_JSON_BLOCK",
            "raw_output": decoded
        }

    raw_json = match.group()

    try:
        return json.loads(raw_json)
    except Exception:
        try:
            normalized = _normalize_json_like(raw_json)
            return json.loads(normalized)
        except Exception:
            return {
                "status": "FAILED",
                "reason": "INVALID_JSON",
                "raw_output": raw_json
            }

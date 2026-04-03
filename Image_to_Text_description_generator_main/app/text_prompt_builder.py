def build_json_prompt(description_text: str, language: str) -> str:
    prompt = (
        "Convert the following product description into STRICT JSON only.\n"
        "Return ONLY a valid JSON object. No explanations. No markdown.\n\n"
        "Description:\n"
        '"""\n'
        f"{description_text}\n"
        '"""\n\n'
        "JSON schema:\n"
        "{\n"
        '  "title": "string",\n'
        '  "short_description": "string",\n'
        '  "long_description": "string",\n'
        '  "bullet_points": ["string"],\n'
        '  "attributes": {\n'
        '    "color": "string",\n'
        '    "material": "string",\n'
        '    "pattern": "string",\n'
        '    "category": "string"\n'
        "  }\n"
        "}\n\n"
        f"Language: {language}\n"
    )

    return prompt

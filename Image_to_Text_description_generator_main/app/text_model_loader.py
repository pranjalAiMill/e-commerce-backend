
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "google/gemma-2-2b-it"

class TextModelLoader:
    _model = None
    _tokenizer = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            cls._tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            cls._model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                torch_dtype=torch.float16,
                device_map="auto"
            ).eval()
        return cls._model, cls._tokenizer

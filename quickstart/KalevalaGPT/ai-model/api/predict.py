"""Model loading and generation using Hugging Face Transformers"""

from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "nraesalmi/tinyllama-kalevala-chat"


class ModelBundle:
    """Container for a tokenizer and a model."""
    def __init__(self, tokenizer, model, device: str):
        self.tokenizer = tokenizer
        self.model = model
        self.device = device


def _select_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_model() -> ModelBundle:
    """Load tokenizer and model with safe defaults."""
    device = _select_device()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto" if device != "cpu" else None,
        trust_remote_code=True,
        torch_dtype="auto" if device != "cpu" else None,
        low_cpu_mem_usage=True,
    )
    model.eval()
    return ModelBundle(tokenizer, model, device)


def _prompt_with_context(user: str, context: str) -> str:
    return (
        "<|system|> You may use the provided context to answer questions. "
        "If not useful, rely on your own knowledge.</s>\n"
        f"<|user|> Context:\n{context}\n\nUser Question:\n{user}</s>\n"
        "<|assistant|>\n"
    )


@torch.inference_mode()
def chat(bundle: ModelBundle, question: str, context: str, max_new_tokens: int = 280) -> str:
    """Generate an answer conditioned on retrieved context."""
    prompt = _prompt_with_context(question, context)
    inputs = bundle.tokenizer(prompt, return_tensors="pt").to(bundle.device)
    output_ids = bundle.model.generate(
        **inputs,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        max_new_tokens=max_new_tokens,
        pad_token_id=bundle.tokenizer.eos_token_id,
    )
    text = bundle.tokenizer.batch_decode(output_ids, skip_special_tokens=False)[0]
    return text.strip()

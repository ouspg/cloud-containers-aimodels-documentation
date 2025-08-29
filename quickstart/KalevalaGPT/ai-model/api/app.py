"""Flask API exposing RAG

Endpoints
---------
GET  /health
POST /query

Usage
-----
$ export FLASK_APP=api.app
$ flask --app ai-model.api.app run --host=0.0.0.0 --port=8000
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS

from .rag import RagService
from .predict import load_model, chat


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


# Init application
app = Flask(__name__)
CORS(app, supports_credentials=True)

API_KEY = os.environ.get("API_KEY")

def check_api_key(req) -> bool:
    """Check if request contains valid API key header."""
    return req.headers.get("x-api-key") == API_KEY

# Initialize heavy components
_rag = RagService()
_model = load_model()

@app.get("/health")
def health() -> Any:
    """Simple health check to verify the service is ready."""

    # Security check
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(
        {
            "status": "ok",
            "embedding_model": _rag.embedding_model,
            "hf_model": os.environ.get("MODEL_NAME", _model.model.config.name_or_path),
            "device": _model.device,
        }
    )


@app.post("/query")
def query() -> Any:
    """Run retrieval, then generate an answer.

    Request JSON
    ------------
    {
      "question": "Who is Wainamoinen?",
      "top_k": 3,                # optional
      "similarity_cutoff": 0.5   # optional
    }

    Response JSON
    -------------
    {
      "answer": "...",
      "context": "Context:\\n ...",
      "sources": ["file1.txt", "file2.txt"],
      "usage": {"top_k": 3, "similarity_cutoff": 0.5}
    }
    """

    # Security check
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    payload: Dict[str, Any] = request.get_json(force=True, silent=False) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    top_k = payload.get("top_k")
    cutoff = payload.get("similarity_cutoff")

    context, sources = _rag.query(question, top_k=top_k, similarity_cutoff=cutoff)
    answer = chat(_model, question, context=context)

    return jsonify(
        {
            "answer": answer,
            "context": context,
            "sources": sources,
            "usage": {
                "top_k": top_k or _rag.top_k_default,
                "similarity_cutoff": cutoff if cutoff is not None else _rag.similarity_cutoff,
            },
        }
    )

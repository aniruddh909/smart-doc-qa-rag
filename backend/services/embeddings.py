# backend/services/embeddings.py

import os
from typing import List
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Fallback to SentenceTransformers if OpenAI key is missing
local_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> List[float]:
    """
    Generate an embedding for the given text.
    Tries OpenAI first, falls back to local model if API key not set.
    """
    if client:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    else:
        return local_model.encode(text).tolist()

def batch_get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    """
    return [get_embedding(t) for t in texts]

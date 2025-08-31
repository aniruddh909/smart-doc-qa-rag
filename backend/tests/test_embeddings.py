# tests/test_embeddings.py

from backend.services.embeddings import get_embedding, batch_get_embeddings

def test_single_embedding():
    text = "Hello, embeddings!"
    vec = get_embedding(text)
    assert isinstance(vec, list)
    assert len(vec) > 0

def test_batch_embeddings():
    texts = ["AI is great.", "Machine learning is powerful."]
    vecs = batch_get_embeddings(texts)
    assert isinstance(vecs, list)
    assert len(vecs) == 2
    assert all(isinstance(v, list) for v in vecs)

# backend/tests/test_embedding_service.py

import pytest
import tempfile
import os
from backend.services.embedding_service import EmbeddingService, DocumentChunk

@pytest.fixture
def embedding_service():
    """Create a fresh embedding service for each test."""
    return EmbeddingService()

@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        DocumentChunk(
            content="This is a test document about artificial intelligence and machine learning.",
            metadata={"source": "test1.txt", "type": "text"}
        ),
        DocumentChunk(
            content="Python is a programming language widely used in data science and AI development.",
            metadata={"source": "test2.txt", "type": "text"}
        ),
        DocumentChunk(
            content="FastAPI is a modern web framework for building APIs with Python.",
            metadata={"source": "test3.txt", "type": "text"}
        )
    ]

def test_chunk_text(embedding_service):
    """Test text chunking functionality."""
    text = "This is a short text."
    chunks = embedding_service.chunk_text(text, chunk_size=50)
    assert len(chunks) == 1
    assert chunks[0] == text
    
    # Test with longer text
    long_text = "This is a very long text. " * 100
    chunks = embedding_service.chunk_text(long_text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(len(chunk) <= 120 for chunk in chunks)  # chunk_size + some tolerance

def test_create_vector_store(embedding_service, sample_documents):
    """Test vector store creation."""
    vector_store = embedding_service.create_vector_store(sample_documents)
    assert vector_store is not None
    assert embedding_service.vector_store is not None

def test_create_vector_store_empty_documents(embedding_service):
    """Test vector store creation with empty documents."""
    with pytest.raises(ValueError, match="No documents provided"):
        embedding_service.create_vector_store([])

def test_query_vector_store(embedding_service, sample_documents):
    """Test querying the vector store."""
    # Create vector store first
    embedding_service.create_vector_store(sample_documents)
    
    # Query for AI-related content
    results = embedding_service.query_vector_store("artificial intelligence", k=2)
    assert len(results) <= 2
    assert all(len(result) == 2 for result in results)  # (document, score) tuples
    
    # Check that scores are reasonable (lower is better for FAISS)
    scores = [score for _, score in results]
    assert all(score >= 0 for score in scores)

def test_query_vector_store_not_initialized(embedding_service):
    """Test querying without initializing vector store."""
    with pytest.raises(ValueError, match="Vector store not initialized"):
        embedding_service.query_vector_store("test query")

def test_get_relevant_context(embedding_service, sample_documents):
    """Test getting relevant context."""
    embedding_service.create_vector_store(sample_documents)
    
    context = embedding_service.get_relevant_context("Python programming", k=2)
    assert isinstance(context, str)
    assert len(context) > 0
    assert "Python" in context or "programming" in context

def test_get_relevant_context_no_results(embedding_service):
    """Test getting context when no documents are available."""
    # Don't create vector store
    embedding_service.vector_store = None
    
    with pytest.raises(ValueError, match="Vector store not initialized"):
        embedding_service.get_relevant_context("test query")

def test_backward_compatibility_functions():
    """Test legacy embedding functions."""
    from backend.services.embedding_service import get_embedding, batch_get_embeddings
    
    # Test single embedding
    embedding = get_embedding("test text")
    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(x, float) for x in embedding)
    
    # Test batch embeddings
    texts = ["text 1", "text 2", "text 3"]
    embeddings = batch_get_embeddings(texts)
    assert len(embeddings) == len(texts)
    assert all(isinstance(emb, list) for emb in embeddings)

def test_long_document_chunking(embedding_service):
    """Test chunking of long documents."""
    long_content = "This is a sentence. " * 200  # Create long text
    doc = DocumentChunk(
        content=long_content,
        metadata={"source": "long_doc.txt"}
    )
    
    vector_store = embedding_service.create_vector_store([doc])
    assert vector_store is not None
    
    # Should create multiple chunks
    chunks = embedding_service.chunk_text(long_content, chunk_size=500)
    assert len(chunks) > 1

def test_metadata_preservation(embedding_service, sample_documents):
    """Test that metadata is preserved in vector store."""
    embedding_service.create_vector_store(sample_documents)
    
    results = embedding_service.query_vector_store("test", k=3)
    
    for doc, score in results:
        assert "source" in doc.metadata
        assert "type" in doc.metadata
        assert doc.metadata["type"] == "text"

# backend/tests/test_qa_router.py

import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from backend.main import app
from backend.routers.qa_router import uploaded_documents
from backend.services.embedding_service import embedding_service

# Create test client
client = TestClient(app)

@pytest.fixture
def cleanup_after_test():
    """Clean up after each test."""
    yield
    # Clear uploaded documents and vector store after each test
    uploaded_documents.clear()
    embedding_service.vector_store = None

def test_health_endpoint(cleanup_after_test):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "embedding_service" in data
    assert "vector_store" in data

def test_upload_text_file(cleanup_after_test):
    """Test uploading a text file."""
    # Create a temporary text file
    test_content = "This is a test document about artificial intelligence and machine learning."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_file_path, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["filename"] == "test.txt"
        assert data["chunks_created"] >= 1
        assert "message" in data
        
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_upload_unsupported_file_type(cleanup_after_test):
    """Test uploading an unsupported file type."""
    test_content = "This is a test file"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("test.xyz", f, "application/octet-stream")}
            )
        
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]
        
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_upload_empty_file(cleanup_after_test):
    """Test uploading an empty file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write("")  # Empty file
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("empty.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
        
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_query_without_documents(cleanup_after_test):
    """Test querying when no documents are uploaded."""
    response = client.post(
        "/api/query",
        json={"query": "What is artificial intelligence?", "k": 3}
    )
    
    assert response.status_code == 400
    assert "No documents uploaded" in response.json()["detail"]

def test_full_upload_and_query_workflow(cleanup_after_test):
    """Test the complete workflow: upload document then query."""
    # Step 1: Upload a document
    test_content = "Artificial intelligence (AI) is a branch of computer science that aims to create intelligent machines. Machine learning is a subset of AI that enables computers to learn from data."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_file_path, 'rb') as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": ("ai_document.txt", f, "text/plain")}
            )
        
        assert upload_response.status_code == 200
        
        # Step 2: Query the document
        query_response = client.post(
            "/api/query",
            json={"query": "What is artificial intelligence?", "k": 2}
        )
        
        assert query_response.status_code == 200
        data = query_response.json()
        
        assert data["query"] == "What is artificial intelligence?"
        assert isinstance(data["context"], str)
        assert len(data["context"]) > 0
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert len(data["sources"]) >= 1
        
        # Check source information
        source = data["sources"][0]
        assert "source" in source
        assert "similarity_score" in source
        assert "preview" in source
        
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_list_documents_empty(cleanup_after_test):
    """Test listing documents when none are uploaded."""
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["total_documents"] == 0
    assert data["documents"] == []

def test_list_documents_with_uploads(cleanup_after_test):
    """Test listing documents after uploading."""
    # Upload a document first
    test_content = "Test document content for listing."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": ("list_test.txt", f, "text/plain")}
            )
        assert upload_response.status_code == 200
        
        # List documents
        response = client.get("/api/documents")
        assert response.status_code == 200
        data = response.json()
        assert data["total_documents"] == 1
        assert len(data["documents"]) == 1
        assert data["documents"][0]["filename"] == "list_test.txt"
        
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_clear_documents(cleanup_after_test):
    """Test clearing all documents."""
    # Upload a document first
    test_content = "Document to be cleared."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": ("clear_test.txt", f, "text/plain")}
            )
        assert upload_response.status_code == 200
        
        # Clear documents
        clear_response = client.delete("/api/documents")
        assert clear_response.status_code == 200
        assert "cleared successfully" in clear_response.json()["message"]
        
        # Verify documents are cleared
        list_response = client.get("/api/documents")
        assert list_response.json()["total_documents"] == 0
        
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_query_with_custom_k_parameter(cleanup_after_test):
    """Test querying with custom k parameter."""
    # Upload a document first
    test_content = "This document contains information about Python programming, artificial intelligence, and web development."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": ("k_test.txt", f, "text/plain")}
            )
        assert upload_response.status_code == 200
        
        # Query with k=1
        query_response = client.post(
            "/api/query",
            json={"query": "programming", "k": 1}
        )
        
        assert query_response.status_code == 200
        data = query_response.json()
        assert len(data["sources"]) <= 1
        
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

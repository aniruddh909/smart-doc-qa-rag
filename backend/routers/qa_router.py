# backend/routers/qa_router.py

import os
import tempfile
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.utils.file_parser import parse_file
from backend.services.embedding_service import embedding_service, DocumentChunk

router = APIRouter(prefix="/api", tags=["Q&A"])

class QueryRequest(BaseModel):
    query: str
    k: int = 3  # Number of top documents to retrieve

class QueryResponse(BaseModel):
    query: str
    context: str
    answer: str  # Will be a stub for now
    sources: List[Dict[str, Any]]

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int
    status: str

# In-memory storage for document metadata (in production, use a database)
uploaded_documents: List[Dict[str, Any]] = []

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document, parse it, create embeddings, and store in FAISS.
    
    Supports: PDF, DOCX, TXT files.
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        supported_extensions = ['.pdf', '.docx', '.txt']
        
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Supported: {', '.join(supported_extensions)}"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse the document
            parsed_content = parse_file(temp_file_path)
            
            if not parsed_content.strip():
                raise HTTPException(status_code=400, detail="Document appears to be empty")
            
            # Create document chunk with metadata
            doc_metadata = {
                "source": file.filename,
                "file_type": file_extension,
                "size": len(content),
                "upload_timestamp": str(os.path.getmtime(temp_file_path))
            }
            
            document_chunk = DocumentChunk(
                content=parsed_content,
                metadata=doc_metadata
            )
            
            # Create or update vector store
            if embedding_service.vector_store is None:
                # First document - create new vector store
                vector_store = embedding_service.create_vector_store([document_chunk])
            else:
                # Add to existing vector store
                # For now, we'll recreate the store (in production, use add_documents)
                # Get existing documents and add new one
                existing_docs = uploaded_documents.copy()
                all_doc_chunks = [document_chunk]
                
                # Recreate vector store with all documents
                vector_store = embedding_service.create_vector_store(all_doc_chunks)
            
            # Calculate chunks created
            chunks_created = len(embedding_service.chunk_text(parsed_content))
            
            # Store document metadata
            doc_info = {
                "filename": file.filename,
                "metadata": doc_metadata,
                "chunks": chunks_created,
                "content_length": len(parsed_content)
            }
            uploaded_documents.append(doc_info)
            
            return UploadResponse(
                message="Document uploaded and processed successfully",
                filename=file.filename,
                chunks_created=chunks_created,
                status="success"
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query the uploaded documents and return relevant context + answer stub.
    """
    try:
        # Check if we have any documents
        if embedding_service.vector_store is None:
            raise HTTPException(
                status_code=400, 
                detail="No documents uploaded yet. Please upload documents first."
            )
        
        # Get relevant context
        context = embedding_service.get_relevant_context(request.query, k=request.k)
        
        # Get detailed results for source information
        results = embedding_service.query_vector_store(request.query, k=request.k)
        
        sources = []
        for doc, score in results:
            source_info = {
                "source": doc.metadata.get("source", "Unknown"),
                "chunk_id": doc.metadata.get("chunk_id", 0),
                "similarity_score": float(score),
                "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            }
            sources.append(source_info)
        
        # Generate answer stub (placeholder for now - later integrate with LLM)
        answer_stub = f"Based on the provided context about '{request.query}', I found {len(sources)} relevant sections. " \
                     f"[This is a stub response - LLM integration coming next]"
        
        return QueryResponse(
            query=request.query,
            context=context,
            answer=answer_stub,
            sources=sources
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")

@router.get("/documents")
async def list_documents():
    """
    List all uploaded documents with metadata.
    """
    return {
        "total_documents": len(uploaded_documents),
        "documents": uploaded_documents
    }

@router.delete("/documents")
async def clear_documents():
    """
    Clear all uploaded documents and reset vector store.
    """
    global uploaded_documents
    uploaded_documents.clear()
    embedding_service.vector_store = None
    
    return {"message": "All documents cleared successfully"}

@router.get("/health")
async def health_check():
    """
    Health check for the Q&A router.
    """
    return {
        "status": "healthy",
        "embedding_service": "initialized",
        "vector_store": "ready" if embedding_service.vector_store else "empty",
        "documents_count": len(uploaded_documents)
    }

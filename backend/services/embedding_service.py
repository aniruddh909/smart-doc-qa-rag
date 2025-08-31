# backend/services/embedding_service.py

import os
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from sentence_transformers import SentenceTransformer

@dataclass
class DocumentChunk:
    """Represents a chunk of text from a document."""
    content: str
    metadata: Dict[str, Any]

class EmbeddingService:
    """Service for handling document embeddings and vector storage."""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize embeddings (OpenAI if available, otherwise local model)
        if self.openai_api_key:
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=self.openai_api_key
            )
            self.embedding_dimension = 1536  # text-embedding-3-small dimension
        else:
            # Fallback to local model
            self._local_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.embeddings = None
            self.embedding_dimension = 384  # all-MiniLM-L6-v2 dimension
        
        self.vector_store: Optional[FAISS] = None
    
    def _get_local_embedding(self, text: str) -> List[float]:
        """Get embedding using local model as fallback."""
        return self._local_model.encode(text).tolist()
    
    def _batch_get_local_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts using local model."""
        return self._local_model.encode(texts).tolist()
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence or paragraph boundaries
            if end < len(text):
                # Look for sentence ending within the last 100 characters
                for i in range(min(100, chunk_size // 2)):
                    if text[end - i - 1] in '.!?\n':
                        end = end - i
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def create_vector_store(self, documents: List[DocumentChunk]) -> FAISS:
        """Create FAISS vector store from documents."""
        if not documents:
            raise ValueError("No documents provided")
        
        # Convert to LangChain Document format
        langchain_docs = []
        for doc in documents:
            # Chunk the document content
            chunks = self.chunk_text(doc.content)
            
            for i, chunk in enumerate(chunks):
                metadata = doc.metadata.copy()
                metadata['chunk_id'] = i
                metadata['total_chunks'] = len(chunks)
                
                langchain_docs.append(Document(
                    page_content=chunk,
                    metadata=metadata
                ))
        
        # Create vector store
        if self.embeddings:
            # Use OpenAI embeddings
            self.vector_store = FAISS.from_documents(langchain_docs, self.embeddings)
        else:
            # Use local embeddings
            texts = [doc.page_content for doc in langchain_docs]
            embeddings_list = self._batch_get_local_embeddings(texts)
            
            # Create FAISS index manually
            import faiss
            dimension = self.embedding_dimension
            index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings to index
            embeddings_array = np.array(embeddings_list).astype('float32')
            index.add(embeddings_array)
            
            # Create FAISS wrapper
            from langchain_community.docstore.in_memory import InMemoryDocstore
            
            docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(langchain_docs)})
            index_to_docstore_id = {i: str(i) for i in range(len(langchain_docs))}
            
            self.vector_store = FAISS(
                embedding_function=self._get_local_embedding,
                index=index,
                docstore=docstore,
                index_to_docstore_id=index_to_docstore_id
            )
        
        return self.vector_store
    
    def query_vector_store(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Query the vector store and return top-k similar documents with scores."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        # Perform similarity search with scores
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        return results
    
    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Get relevant context for a query as a concatenated string."""
        results = self.query_vector_store(query, k=k)
        
        if not results:
            return "No relevant context found."
        
        context_parts = []
        for doc, score in results:
            # Include metadata if available
            source = doc.metadata.get('source', 'Unknown')
            context_parts.append(f"[Source: {source}]\n{doc.page_content}")
        
        return "\n\n---\n\n".join(context_parts)

# Global service instance
embedding_service = EmbeddingService()

# Backward compatibility functions
def get_embedding(text: str) -> List[float]:
    """Legacy function for getting a single embedding."""
    if embedding_service.embeddings:
        return embedding_service.embeddings.embed_query(text)
    else:
        return embedding_service._get_local_embedding(text)

def batch_get_embeddings(texts: List[str]) -> List[List[float]]:
    """Legacy function for getting multiple embeddings."""
    if embedding_service.embeddings:
        return embedding_service.embeddings.embed_documents(texts)
    else:
        return embedding_service._batch_get_local_embeddings(texts)

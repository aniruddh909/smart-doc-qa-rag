# Smart Document Q&A with RAG

A comprehensive document question-answering system built with Retrieval-Augmented Generation (RAG) architecture. This application allows users to upload documents and ask natural language questions, receiving intelligent answers based on the document content.

https://github.com/aniruddh909/smart-doc-qa-rag/blob/main/frontend/ss.png?raw=true<img width="1620" height="737" alt="image" src="https://github.com/user-attachments/assets/9c3498ae-94b8-48ed-9b57-70544b92a1d4" />

## Overview

This project implements a full-stack RAG system that combines document processing, vector search, and AI-powered question answering. Users can upload PDF, DOCX, or TXT files through a modern React interface and query their content using natural language questions.

## Architecture

The system consists of three main components:

1. **Document Processing Pipeline**: Extracts and chunks text from uploaded documents
2. **Vector Search Engine**: Uses FAISS for fast similarity search across document embeddings
3. **AI Answer Generation**: Leverages Hugging Face transformers to generate contextual answers

## Tech Stack

### Backend

- **FastAPI**: High-performance Python web framework for API development
- **LangChain**: Framework for building applications with large language models
- **Hugging Face Transformers**: Pre-trained models for natural language processing
- **FAISS**: Facebook AI Similarity Search for efficient vector operations
- **Embedding Models**: Sentence transformers for document vectorization

### Frontend

- **React 18**: Modern JavaScript library for building user interfaces
- **Axios**: HTTP client for API communication
- **Lucide React**: Icon library for consistent UI elements
- **CSS3**: Custom styling with gradients and animations

### Document Processing

- **pypdf**: PDF text extraction and processing
- **python-docx**: Microsoft Word document parsing
- **Text Processing**: Built-in support for plain text files

### Development Tools

- **Pytest**: Comprehensive testing framework
- **Git**: Version control with organized commit history
- **npm**: Package management for frontend dependencies

## Features

### Document Management

- Support for multiple file formats (PDF, DOCX, TXT)
- Drag-and-drop file upload interface
- Automatic text extraction and preprocessing
- Document metadata tracking and storage

### Intelligent Query System

- Natural language question processing
- Contextual answer generation using AI models
- Relevance scoring for retrieved information
- Source attribution for transparency

### User Interface

- Modern, responsive web interface
- Real-time feedback and loading states
- Tabbed results display (AI answers and document context)
- Sample questions to guide user interaction
- Copy-to-clipboard functionality for answers

### Technical Capabilities

- Vector-based semantic search
- Text chunking with overlap for better context
- Fallback model support for different hardware configurations
- Comprehensive error handling and validation
- RESTful API design with clear endpoints

## API Endpoints

### Core Functionality

- `POST /api/upload` - Upload and process documents
- `POST /api/query` - Submit questions and receive AI-generated answers
- `GET /api/documents` - List all uploaded documents with metadata
- `DELETE /api/documents` - Clear all documents and reset vector store
- `GET /api/health` - System health check for Q&A functionality

### System Endpoints

- `GET /health` - Main application health check
- `GET /` - Root endpoint with health redirect

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Git for version control

1. Clone the repository
2. Navigate to the project directory
3. Create a Python virtual environment
4. Install Python dependencies from requirements.txt
5. Run the FastAPI server using uvicorn




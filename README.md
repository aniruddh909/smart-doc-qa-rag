# Smart Document Q&A with RAG

A comprehensive document question-answering system built with Retrieval-Augmented Generation (RAG) architecture. This application allows users to upload documents and ask natural language questions, receiving intelligent answers based on the document content.

## Overview

This project implements a full-stack RAG system that combines document processing, vector search, and AI-powered question answering. Users can upload PDF, DOCX, or TXT files through a modern React interface and query their content using natural language questions.

## Architecture

The system consists of three main components:

1. **Document Processing Pipeline**: Extracts and chunks text from uploaded documents
2. **Vector Search Engine**: Uses FAISS for fast similarity search across document embeddings
3. **AI Answer Generation**: Leverages Hugging Face transformers to generate contextual answers

## Technology Stack

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

### Backend Setup
1. Clone the repository
2. Navigate to the project directory
3. Create a Python virtual environment
4. Install Python dependencies from requirements.txt
5. Run the FastAPI server using uvicorn

### Frontend Setup
1. Navigate to the frontend directory
2. Install Node.js dependencies using npm
3. Start the React development server
4. Access the application through your web browser

### Development Environment
The application uses a proxy configuration to connect the React frontend (port 3000) with the FastAPI backend (port 8000), enabling seamless development and testing.

## Usage Workflow

### Document Upload
1. Access the web interface through your browser
2. Use the drag-and-drop area or click to select files
3. Upload PDF, DOCX, or TXT documents
4. Wait for processing completion confirmation

### Querying Documents
1. Enter natural language questions in the query interface
2. Use provided sample questions or create custom queries
3. Receive AI-generated answers with supporting context
4. View source information and relevance scores
5. Copy answers to clipboard for external use

### Results Interpretation
- **AI Answers Tab**: Generated responses based on document content
- **Context Tab**: Relevant text excerpts from source documents
- **Relevance Scores**: Numerical indicators of content similarity
- **Source Attribution**: Document names and locations for verification

## Testing

The project includes a comprehensive test suite covering:

- File parsing functionality for all supported formats
- Embedding generation and vector store operations
- API endpoint validation and error handling
- Answer generation quality and consistency
- Frontend component behavior and integration

Run tests using the pytest command with verbose output for detailed results.

## Project Structure

```
smart-doc-qa-rag/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── routers/                # API route definitions
│   ├── services/               # Core business logic
│   ├── utils/                  # Utility functions
│   └── tests/                  # Test suite
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.js             # Main application component
│   │   └── index.js           # React entry point
│   ├── public/                # Static assets
│   └── package.json           # Frontend dependencies
├── docs/                      # Project documentation
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Development Guidelines

### Code Quality
- Maintain comprehensive test coverage for new features
- Follow consistent naming conventions and code structure
- Include error handling and input validation
- Document complex algorithms and business logic

### Git Workflow
- Create meaningful commit messages with clear descriptions
- Keep commits focused on single features or fixes
- Update documentation when adding new functionality
- Run tests before committing changes

### Performance Considerations
- Optimize vector search operations for large document collections
- Implement efficient text chunking strategies
- Monitor memory usage with large language models
- Cache frequently accessed embeddings when possible

## Contributing

This project welcomes contributions in the form of bug reports, feature suggestions, and code improvements. Please ensure all changes include appropriate tests and documentation updates.

## Future Enhancements

- Integration with additional AI model providers
- Advanced document format support (presentations, spreadsheets)
- Multi-language document processing capabilities
- User authentication and document access controls
- Deployment automation with Docker containers
- Scalable vector database integration (Pinecone, Weaviate)
- Enhanced UI with advanced filtering and search options

## License

This project is developed for educational and research purposes, demonstrating modern RAG architecture implementation with practical document processing capabilities.
# Frontend - Smart Document Q&A

A React-based frontend for the Smart Document Q&A system with RAG (Retrieval Augmented Generation).

## Features

- **📤 Document Upload**: Drag & drop or click to upload PDF, DOCX, TXT files
- **❓ Interactive Querying**: Ask natural language questions about uploaded documents
- **🤖 AI Answers**: Get AI-generated responses using Hugging Face models
- **📚 Context Display**: View retrieved document chunks and source references
- **📱 Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js 16+
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at http://localhost:3000

### Usage

1. **Upload Documents**: Drag and drop or click to select PDF, DOCX, or TXT files
2. **Ask Questions**: Type your question in the query box or use sample questions
3. **View Results**: Toggle between AI Answer and Context tabs to see responses and sources

## Components

- **App.js** - Main application component
- **DocumentUpload.js** - File upload interface with drag & drop
- **QueryInterface.js** - Question input with sample prompts
- **ResultsDisplay.js** - Tabbed display for answers and context

## API Integration

The frontend communicates with the backend API:

- `POST /api/upload` - Upload documents
- `POST /api/query` - Ask questions
- `GET /api/documents` - List uploaded files
- `DELETE /api/documents` - Clear all documents

## Technologies

- **React 18** - UI framework
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **CSS3** - Modern styling with gradients and animations

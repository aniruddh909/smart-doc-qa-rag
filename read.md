# Smart Document Q&A with RAG

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React (React Flow planned)
- **AI**: LangChain for embeddings & RAG (Retrieval Augmented Generation)
- **LLMs**: Hugging Face Transformers (google/flan-t5-base) + OpenAI (optional)
- **Vector DB**: FAISS (in-memory for now, later scalable options like Pinecone or Weaviate)
- **Parsing**: pypdf (migrated from PyPDF2), python-docx, plain text parsing
- **Testing**: Pytest

## API Endpoints

### Core Q&A Endpoints

- **POST `/api/upload`** - Upload and process documents (PDF, DOCX, TXT)
  - Returns: Document metadata, chunk count, processing status
- **POST `/api/query`** - Query documents with natural language
  - Request: `{"query": "your question", "k": 3}`
  - Returns: Query, relevant context, AI-generated answer, similarity sources
- **GET `/api/documents`** - List all uploaded documents with metadata
- **DELETE `/api/documents`** - Clear all documents and reset vector store
- **GET `/api/health`** - Health check for Q&A system

### System Endpoints

- **GET `/health`** - Main health check
- **GET `/`** - Redirects to `/health`

## Current Progress

- File parsing module (`backend/utils/file_parser.py`)
  - Supports `.pdf`, `.docx`, `.txt`
  - **FIXED**: Migrated from PyPDF2 to pypdf library
- **FIXED**: File parser tests now use proper `tmp_path` fixtures
  - 9 comprehensive tests covering txt, pdf, docx parsing
  - Tests for error handling and edge cases
- **NEW**: Embedding + FAISS integration (`backend/services/embedding_service.py`)
  - LangChain OpenAI embeddings with local fallback (SentenceTransformers)
  - FAISS vector store for document retrieval
  - Smart text chunking with overlap
  - Functions: `create_vector_store()`, `query_vector_store()`, `get_relevant_context()`
- ✅ **COMPLETED**: FastAPI routes (`backend/routers/qa_router.py`)
  - `/api/upload` - Upload and process documents (PDF, DOCX, TXT)
  - `/api/query` - Query documents and get relevant context + AI-generated answer
  - `/api/documents` - List uploaded documents
  - `/api/health` - Health check for Q&A system
- ✅ **NEW**: AI Answer Generation (`backend/services/answer_generator.py`)
  - **Hugging Face Transformers integration** with `google/flan-t5-base`
  - Fallback to smaller models if GPU/memory limited
  - Smart prompt engineering for Q&A tasks
  - Answer post-processing and error handling
- ✅ **COMPLETED**: Comprehensive test suite
  - 45+ total tests (file parser + embeddings + API endpoints + answer generation)
  - Test coverage for upload workflow, querying, AI answer generation, error handling
- Repo structured into:
  - `backend/`
  - `backend/tests/`
  - `backend/utils/`
  - `backend/services/`
  - `backend/routers/`
  - `docs/`
  - `requirements.txt`

## TODO (Next Steps)

- ✅ **COMPLETED**: Fix and expand tests (PDF, DOCX, TXT using `tmp_path`)
- ✅ **COMPLETED**: Migrate from PyPDF2 to pypdf library
- ✅ **COMPLETED**: Add embedding + FAISS integration
- ✅ **COMPLETED**: Add FastAPI routes (`/upload`, `/query`, `/documents`)
- ✅ **COMPLETED**: Add comprehensive tests (45+ total tests passing)
- ✅ **COMPLETED**: Integrate Hugging Face LLM for real answer generation (replace answer stub)
- Add OpenAI API integration for better responses
- Setup React frontend (React Flow based)
- Add file upload UI and query interface
- Dockerize project
- Deployment pipeline

## End-to-End RAG Workflow

1. **Upload**: User uploads PDF/DOCX/TXT → File parsing → Text extraction
2. **Embed**: Text chunking → Generate embeddings → Store in FAISS vector database
3. **Query**: User asks question → Similarity search → Retrieve top-k relevant chunks
4. **Generate**: Pass query + context to Hugging Face model → Generate natural language answer
5. **Return**: JSON response with answer, context, and source references

---

## Rules for Co-Pilot

- Always update this file (`PROJECT_SUMMARY.md`) whenever functionality changes.
- Always run tests (`pytest backend/tests -v`) after backend changes.
- Keep commits small and meaningful.
- Update the repo frequently: `git add . && git commit -m "msg" && git push`.

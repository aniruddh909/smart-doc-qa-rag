# Smart Document Q&A with RAG

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React (React Flow planned)
- **AI**: LangChain for embeddings & RAG (Retrieval Augmented Generation)
- **LLMs**: OpenAI (can switch later)
- **Vector DB**: FAISS (in-memory for now, later scalable options like Pinecone or Weaviate)
- **Parsing**: pypdf (migrated from PyPDF2), python-docx, plain text parsing
- **Testing**: Pytest

## Current Progress

- File parsing module (`backend/utils/file_parser.py`)
  - Supports `.pdf`, `.docx`, `.txt`
  - **FIXED**: Migrated from PyPDF2 to pypdf library
- **FIXED**: File parser tests now use proper `tmp_path` fixtures
  - 9 comprehensive tests covering txt, pdf, docx parsing
  - Tests for error handling and edge cases
- Embedding logic partially started
- Repo structured into:
  - `backend/`
  - `backend/tests/`
  - `backend/utils/`
  - `docs/`
  - `requirements.txt`

## TODO (Next Steps)

- ✅ **COMPLETED**: Fix and expand tests (PDF, DOCX, TXT using `tmp_path`)
- ✅ **COMPLETED**: Migrate from PyPDF2 to pypdf library
- Add embedding + FAISS integration
- Add FastAPI routes:
  - `/upload` for documents
  - `/query` for Q&A
- Integrate LangChain for retrieval
- Setup React frontend (React Flow based)
- Dockerize project
- Deployment pipeline

---

## Rules for Co-Pilot

- Always update this file (`PROJECT_SUMMARY.md`) whenever functionality changes.
- Always run tests (`pytest backend/tests -v`) after backend changes.
- Keep commits small and meaningful.
- Update the repo frequently: `git add . && git commit -m "msg" && git push`.

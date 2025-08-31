from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from backend.routers.qa_router import router as qa_router

load_dotenv()

app = FastAPI(
    title="Smart Document Q&A with RAG",
    description="AI-powered document question answering using Retrieval Augmented Generation",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(qa_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health_check():
    return {
        "status": "ok", 
        "message": "Smart Document Q&A API is running",
        "version": "1.0.0"
    }
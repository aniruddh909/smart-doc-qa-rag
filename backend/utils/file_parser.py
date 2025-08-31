import os
from typing import List
from pypdf import PdfReader
from docx import Document


def parse_pdf(file_path: str) -> str:
    """Extract text from PDF."""
    text = []
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {e}")
    return "\n".join(text)

def parse_docx(file_path: str) -> str:
    """Extract text from DOCX."""
    text = []
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text)
    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX: {e}")
    return "\n".join(text)

def parse_txt(file_path: str) -> str:
    """Extract text from TXT."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to parse TXT: {e}")

def parse_file(file_path: str) -> str:
    """Generic function to parse a file based on extension."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

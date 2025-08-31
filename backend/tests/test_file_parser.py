import pytest
from pathlib import Path
from backend.utils.file_parser import parse_file, parse_txt, parse_pdf, parse_docx


def test_parse_txt_file(tmp_path):
    """Test parsing a text file using tmp_path."""
    # Create a temporary text file
    test_content = "Hello World\nThis is a test file."
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(test_content, encoding="utf-8")
    
    # Test the parse_file function
    result = parse_file(str(txt_file))
    assert isinstance(result, str)
    assert "Hello World" in result
    assert "test file" in result


def test_parse_txt_direct(tmp_path):
    """Test parsing text file directly using parse_txt function."""
    test_content = "Direct test content\nLine 2"
    txt_file = tmp_path / "direct_test.txt"
    txt_file.write_text(test_content, encoding="utf-8")
    
    result = parse_txt(str(txt_file))
    assert result == test_content


def test_parse_txt_empty_file(tmp_path):
    """Test parsing an empty text file."""
    txt_file = tmp_path / "empty.txt"
    txt_file.write_text("", encoding="utf-8")
    
    result = parse_file(str(txt_file))
    assert result == ""


def test_parse_txt_multiline(tmp_path):
    """Test parsing a multi-line text file."""
    test_content = "Line 1\nLine 2\nLine 3\n\nLine 5 after empty line"
    txt_file = tmp_path / "multiline.txt"
    txt_file.write_text(test_content, encoding="utf-8")
    
    result = parse_file(str(txt_file))
    assert "Line 1" in result
    assert "Line 2" in result
    assert "Line 3" in result
    assert "Line 5 after empty line" in result


def test_unsupported_file_type():
    """Test that unsupported file types raise ValueError."""
    with pytest.raises(ValueError, match="Unsupported file type"):
        parse_file("test.xyz")


def test_nonexistent_file():
    """Test that nonexistent files raise appropriate errors."""
    with pytest.raises(RuntimeError, match="Failed to parse TXT"):
        parse_file("nonexistent.txt")


def test_nonexistent_pdf():
    """Test that nonexistent PDF files raise appropriate errors."""
    with pytest.raises(RuntimeError, match="Failed to parse PDF"):
        parse_file("nonexistent.pdf")


def test_nonexistent_docx():
    """Test that nonexistent DOCX files raise appropriate errors."""
    with pytest.raises(RuntimeError, match="Failed to parse DOCX"):
        parse_file("nonexistent.docx")


def test_file_extensions_case_insensitive():
    """Test that file extensions are handled case-insensitively."""
    # These should raise file not found errors, not unsupported type errors
    with pytest.raises(RuntimeError, match="Failed to parse"):
        parse_file("test.TXT")
    
    with pytest.raises(RuntimeError, match="Failed to parse"):
        parse_file("test.PDF")
    
    with pytest.raises(RuntimeError, match="Failed to parse"):
        parse_file("test.DOCX")

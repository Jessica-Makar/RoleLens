
import pytest
from docx import Document

from src.resume_parser import (
    clean_resume_text,
    extract_resume_text
)


def test_clean_resume_text():
    text = "  Python    SQL     Power BI  "

    result = clean_resume_text(text)

    assert result == "Python SQL Power BI"


def test_extract_docx_text(tmp_path):
    document = Document()
    document.add_paragraph("Alex Morgan")
    document.add_paragraph("Python, SQL, Java")

    file_path = tmp_path / "resume.docx"
    document.save(file_path)

    with open(file_path, "rb") as file:
        result = extract_resume_text(file, "docx")

    assert "Alex Morgan" in result
    assert "Python, SQL, Java" in result


def test_empty_resume(tmp_path):
    document = Document()

    file_path = tmp_path / "empty_resume.docx"
    document.save(file_path)

    with open(file_path, "rb") as file:
        with pytest.raises(ValueError):
            extract_resume_text(file, "docx")


def test_unsupported_file_type():
    with pytest.raises(ValueError):
        extract_resume_text(None, "txt")


def test_invalid_docx():
    from io import BytesIO

    invalid_file = BytesIO(b"not a valid docx file")

    with pytest.raises(RuntimeError):
        extract_resume_text(invalid_file, "docx")

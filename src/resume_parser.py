
import re

from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    """Extract text from a PDF resume."""

    pdf = PdfReader(file)
    extracted_text = []

    for page in pdf.pages:
        text = page.extract_text()

        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)


def extract_docx_text(file):
    """Extract text from a DOCX resume."""

    document = Document(file)
    extracted_text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_text.append(paragraph.text)

    # Extract text from tables
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    extracted_text.append(cell.text)

    return "\n".join(extracted_text)


def clean_resume_text(text):
    """Clean unnecessary whitespace from resume text."""

    cleaned_text = re.sub(r"[ \t]+", " ", text)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return cleaned_text.strip()



def extract_resume_text(file, file_type):
    """Extract and clean resume text with error handling."""

    try:
        if file_type == "pdf":
            raw_text = extract_pdf_text(file)

        elif file_type == "docx":
            raw_text = extract_docx_text(file)

        else:
            raise ValueError("Unsupported file format.")

        cleaned_text = clean_resume_text(raw_text)

        if not cleaned_text:
            raise ValueError("The uploaded resume contains no readable text.")

        return cleaned_text

    except ValueError:
        raise

    except Exception as error:
        raise RuntimeError(
            f"Unable to process the resume: {error}"
        ) from error



from docx import Document

document = Document()

document.add_heading("Alex Morgan", level=1)
document.add_paragraph("Computer Science Graduate")

document.add_heading("Technical Skills", level=2)
document.add_paragraph("Python, SQL, Java, Power BI")

document.add_heading("Experience", level=2)
document.add_paragraph("IT Support Intern")
document.add_paragraph(
    "Resolved hardware and software issues."
)
document.add_paragraph(
    "Assisted with troubleshooting and documentation."
)

document.add_heading("Education", level=2)
document.add_paragraph("Rutgers University")
document.add_paragraph("B.S. Computer Science")

document.save("data/sample_resumes/sample_resume.docx")

import fitz  # PyMuPDF
from docx import Document
import re


def clean_text(text):
    # Remove non-XML compatible characters
    cleaned_text = re.sub(r'[^\x20-\x7E]', '', text)
    return cleaned_text


def pdf_to_docx(pdf_path, docx_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Create a new DOCX document
    doc = Document()

    # Extract text from each page and add it to the DOCX document
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text = page.get_text()
        cleaned_text = clean_text(text)
        doc.add_paragraph(cleaned_text)

    # Close the PDF document
    pdf_document.close()

    # Save the DOCX document
    doc.save(docx_path)


if __name__ == "__main__":
    pdf_path = r"file_to_convert.pdf"  # Replace with your PDF file path
    docx_path = r"output.docx"  # Replace with your desired output Word file path

    pdf_to_docx(pdf_path, docx_path)
    print(f"Conversion completed. Word document saved to {docx_path}")


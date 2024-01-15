import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup


def pdf_to_html(pdf_path, html_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Create a temporary directory to store images
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    # Save images to the temporary directory
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(temp_dir, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    # Extract text from images using OCR
    text = ""
    for image_path in image_paths:
        text += pytesseract.image_to_string(Image.open(image_path), lang='eng')

    # Clean and format the text into HTML using BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    clean_html = soup.prettify()

    # Save the clean HTML to a file
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(clean_html)

    # Remove temporary image files and directory
    for image_path in image_paths:
        os.remove(image_path)
    os.rmdir(temp_dir)


if __name__ == "__main__":
    pdf_path = "file_to_convert.pdf"  # Replace with your PDF file path
    html_path = "output.html"  # Replace with your desired output HTML file path

    pdf_to_html(pdf_path, html_path)
    print(f"Conversion completed. HTML saved to {html_path}")


# import fitz  # PyMuPDF
# from bs4 import BeautifulSoup
#
#
# def pdf_to_html(pdf_path, html_path):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)
#
#     # Extract text from each page
#     text = ""
#     for page_number in range(pdf_document.page_count):
#         page = pdf_document[page_number]
#         text += page.get_text()
#
#     # Close the PDF document
#     pdf_document.close()
#
#     # Clean and format the text into HTML using BeautifulSoup
#     soup = BeautifulSoup(text, "html.parser")
#     clean_html = soup.prettify()
#
#     # Save the clean HTML to a file
#     with open(html_path, "w", encoding="utf-8") as html_file:
#         html_file.write(clean_html)

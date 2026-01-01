import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text=""
    for page in doc :
        text += str(page.get_text())
        doc.close()
    return text

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
# -*- coding: utf-8 -*-
import pdfplumber
import pytesseract
from PIL import Image
import pdf2image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        if text.strip():
            return text
        else:
            return extract_text_from_image_pdf(file_path)
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_image_pdf(file_path):
    text = ""
    try:
        images = pdf2image.convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error: {str(e)}"
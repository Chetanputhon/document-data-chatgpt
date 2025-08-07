import fitz  # PyMuPDF
import pandas as pd
from PIL import Image
import pytesseract
from docx import Document
import io

def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()
    bytes_data = uploaded_file.read()

    if filename.endswith(".pdf"):
        text = ""
        pdf = fitz.open(stream=bytes_data, filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text

    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(bytes_data))
        return "\n".join([p.text for p in doc.paragraphs])

    elif filename.endswith((".csv", ".xlsx")):
        df = pd.read_csv(io.BytesIO(bytes_data)) if filename.endswith(".csv") else pd.read_excel(io.BytesIO(bytes_data))
        return df.to_string(index=False)

    elif filename.endswith(".txt"):
        return bytes_data.decode("utf-8")

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(bytes_data))
        return pytesseract.image_to_string(image)

    else:
        return "Unsupported file format."
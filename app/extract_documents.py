# extract_documents.py

import os
import uuid
import pandas as pd
import PyPDF2
import docx

base_dir = os.path.dirname(os.path.abspath(__file__))
doc_folder = os.path.join(base_dir, "..", "Documents")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text.strip()

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    return "\n".join(df.astype(str).apply(" ".join, axis=1))

def extract_documents():
    doc_data = {}
    metadata = {}

    for filename in os.listdir(doc_folder):
        file_path = os.path.join(doc_folder, filename)
        ext = filename.split(".")[-1].lower()

        if ext not in ["pdf", "docx", "txt", "csv"]:
            continue

        try:
            if ext == "pdf":
                text = extract_text_from_pdf(file_path)
            elif ext == "docx":
                text = extract_text_from_docx(file_path)
            elif ext == "txt":
                text = extract_text_from_txt(file_path)
            elif ext == "csv":
                text = extract_text_from_csv(file_path)
        except Exception as e:
            print(f"⚠️ Failed to extract from {filename}: {e}")
            continue

        uid = "doc_" + str(uuid.uuid4())[:8]
        doc_data[uid] = text
        metadata[uid] = {
            "filename": filename,
            "extension": ext,
        }

    return doc_data, metadata

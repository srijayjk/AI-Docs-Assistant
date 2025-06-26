import os
from pdfminer.high_level import extract_text
from unstructured.partition.pdf import partition_pdf
import pytesseract
from PIL import Image

def image_to_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def load_text_from_pdf(path):
    try:
        text = extract_text(path)
        if not text.strip():
            raise ValueError("Empty text from PDFMiner")
        return text
    except Exception:
        print(f"[INFO] Using Unstructured/OCR fallback for: {path}")
        elements = partition_pdf(filename=path)
        return "\n".join([e.text for e in elements if e.text])

def load_text_from_image(path):
    return image_to_text(path)

def load_documents_from_folder(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        ext = filename.lower().split(".")[-1]
        full_path = os.path.join(folder_path, filename)

        if ext == "pdf":
            text = load_text_from_pdf(full_path)
        elif ext in ("png", "jpg", "jpeg", "tiff"):
            text = load_text_from_image(full_path)
        else:
            continue

        docs.append((filename, text))
    return docs

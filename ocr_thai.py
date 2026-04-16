import easyocr
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

# Load OCR model ONCE
reader = easyocr.Reader(['th', 'en'])


def extract_text_from_document(file_path):

    ocr_text = ""

    # If PDF
    if file_path.lower().endswith(".pdf"):

        images = convert_from_path(file_path)

        for img in images:
            img_np = np.array(img)
            result = reader.readtext(img_np, detail=0)
            ocr_text += " ".join(result) + " "

    # If Image
    else:

        img = Image.open(file_path)
        img_np = np.array(img)

        result = reader.readtext(img_np, detail=0)
        ocr_text = " ".join(result)

    return ocr_text
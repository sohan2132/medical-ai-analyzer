import json
import sqlite3
import argostranslate.translate
import easyocr
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

from extractor import extract_medical_data
from risk_score import calculate_risk


# ---------------- LOAD OCR MODEL ONCE ----------------
print("Loading EasyOCR model...")
reader = easyocr.Reader(['th', 'en'])
print("OCR model loaded.")


def run_pipeline(input_file):

    print("Starting Medical Report Pipeline...\n")

    # -------- STEP 1: OCR --------
    print("Running OCR...")

    ocr_text = ""

    # If input is PDF
    if input_file.lower().endswith(".pdf"):

        images = convert_from_path(input_file)

        for img in images:
            img_np = np.array(img)
            result = reader.readtext(img_np, detail=0)
            ocr_text += " ".join(result) + " "

    # If input is image
    else:

        img = Image.open(input_file)
        img_np = np.array(img)

        result = reader.readtext(img_np, detail=0)
        ocr_text = " ".join(result)

    thai_text = ocr_text

    print("\nOCR Output:")
    print(thai_text)

    # -------- STEP 2: TRANSLATION --------
    print("\nTranslating Thai → English...")

    english_text = argostranslate.translate.translate(
        thai_text,
        "th",
        "en"
    )

    print("\nTranslated Text:")
    print(english_text)

    # -------- STEP 3: LLM EXTRACTION --------
    print("\nExtracting medical data using Mistral...")

    extracted = extract_medical_data(english_text)

    print("\nRaw Extracted Output:")
    print(extracted)

    # -------- STEP 4: CLEAN JSON --------
    cleaned = extracted.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(cleaned)
    except:
        print("Error parsing JSON")
        return None

    print("\nStructured Data:")
    print(data)

    # -------- STEP 5: RISK SCORE --------
    print("\nCalculating Health Risk Score...")

    score = calculate_risk(data)

    print("\nFinal Risk Score:", score)

    if score < 20:
        decision = "Low Risk - Auto Approve Policy"
    elif score < 50:
        decision = "Medium Risk - Underwriter Review"
    else:
        decision = "High Risk - Further Medical Tests Required"

    print("Decision:", decision)

    # -------- STEP 6: STORE DATA --------
    print("\nSaving data to database...")

    conn = sqlite3.connect("medical_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        age INTEGER,
        diagnosis TEXT,
        blood_pressure TEXT,
        cholesterol TEXT,
        smoking_status TEXT,
        risk_score INTEGER
    )
    """)

    cursor.execute(
        """
        INSERT INTO reports
        (patient_name, age, diagnosis, blood_pressure, cholesterol, smoking_status, risk_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("patient_name"),
            data.get("age"),
            str(data.get("diagnosis")),
            data.get("blood_pressure"),
            data.get("cholesterol"),
            data.get("smoking_status"),
            score
        )
    )

    conn.commit()
    conn.close()

    print("Report stored in database.")
    print("\nPipeline Completed Successfully.")

    return {
        "data": data,
        "score": score,
        "decision": decision
    }
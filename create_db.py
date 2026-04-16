import sqlite3

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

conn.commit()
conn.close()

print("Database created.")
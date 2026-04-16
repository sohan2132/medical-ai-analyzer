import sqlite3

conn = sqlite3.connect("medical_reports.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM reports")

rows = cursor.fetchall()

print("\nStored Medical Reports:\n")

for row in rows:
    print(row)

conn.close()
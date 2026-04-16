import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("medical_reports.db")

# Load data from reports table
df = pd.read_sql_query("SELECT * FROM reports", conn)

# Export to Excel
output_file = "medical_reports_output.xlsx"
df.to_excel(output_file, index=False)

conn.close()

print("Excel report generated successfully:", output_file)
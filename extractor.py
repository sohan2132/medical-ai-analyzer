from dotenv import load_dotenv
import os
from mistralai.client import MistralClient

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("MISTRAL_API_KEY")

# Initialize client
client = MistralClient(api_key=api_key)


def extract_medical_data(text):

    prompt = f"""
You are a medical data extraction assistant.

Extract the following information from the medical report.

Return ONLY valid JSON with these fields:
- patient_name
- age
- diagnosis
- blood_pressure
- cholesterol
- smoking_status

Medical Report:
{text}
"""

    response = client.chat(
        model="mistral-small",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
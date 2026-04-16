def calculate_risk(data):

    score = 0

    age = int(data.get("age",0))

    if age > 50:
        score += 20

    if "diabetes" in str(data).lower():
        score += 30

    if "hypertension" in str(data).lower():
        score += 20

    if "smoking_status" in str(data).lower():
        score += 25

    if "cholesterol" in str(data).lower():
        score += 15

    return score
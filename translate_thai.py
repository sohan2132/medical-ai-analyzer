import argostranslate.translate

def translate_thai_to_english(text):

    translated = argostranslate.translate.translate(
        text,
        "th",
        "en"
    )

    return translated
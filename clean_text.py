from load_pdf import load_all_pdfs
import re

raw_text = load_all_pdfs()

def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9.,!? ]", "", text)
    return text.strip()

cleaned_text = clean_text(raw_text)

print(cleaned_text[:1000])
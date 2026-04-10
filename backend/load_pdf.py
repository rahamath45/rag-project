import os
import subprocess

documents = []

def extract_text(path):
    result = subprocess.run(
        ["pdftotext", "-layout", path, "-"],
        capture_output=True,
        text=True
    )
    return result.stdout


base_path = "data"

for class_folder in os.listdir(base_path):
    class_path = os.path.join(base_path, class_folder)

    if not os.path.isdir(class_path):
        continue

    for file in os.listdir(class_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(class_path, file)

            try:
                text = extract_text(pdf_path)

                documents.append({
                    "text": text,
                    "class": class_folder
                })

                print("Loaded:", file, "->", class_folder)

            except Exception as e:
                print("Error:", file, e)
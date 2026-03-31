import subprocess
import os

def load_all_pdfs():
    text = ""
    base_path = "data"

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".pdf"):
                path = os.path.join(root, file)
                try:
                    result = subprocess.run(
                        ["pdftotext", "-layout", path, "-"],
                        capture_output=True, text=True, timeout=60
                    )
                    if result.returncode == 0:
                        text += result.stdout
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    return text


# 🔥 IMPORTANT: function call
if __name__ == "__main__":
    output = load_all_pdfs()
    with open("extracted_text.txt", "w") as f:
        f.write(output)
    print(f"Saved {len(output)} characters to extracted_text.txt")
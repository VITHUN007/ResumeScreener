import fitz  

def extract_text_from_pdfs(uploaded_files):

    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    combined_text = ""

    for uploaded_file in uploaded_files:
        try:
            uploaded_file.seek(0)  

            file_bytes = uploaded_file.read()

            if not file_bytes:
                continue  

            pdf = fitz.open(stream=file_bytes, filetype="pdf")

            for page in pdf:
                combined_text += page.get_text()

        except Exception as e:
            print(f"Error reading {uploaded_file.name}: {e}")

    return combined_text
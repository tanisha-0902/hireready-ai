import pdfplumber
import re

def extract_text_from_pdf(uploaded_file):
    # uploaded_file is the file object from Streamlit's st.file_uploader
    # pdfplumber opens it like a book and reads every page
    try:
        all_text = ""

        with pdfplumber.open(uploaded_file) as pdf:
            # Loop through every page one by one
            # Think of this like turning each page of the book
            for page in pdf.pages:
                page_text = page.extract_text()

                # Some pages might be empty or unreadable — skip them
                if page_text:
                    all_text += page_text + "\n"

        # If the whole PDF had no readable text, return None
        # This happens with scanned image PDFs
        if not all_text.strip():
            print("WARNING: No text found in PDF. It might be a scanned image.")
            return None

        # Clean the text — remove extra blank lines
        # re.sub replaces patterns. \n{3,} means 3 or more newlines in a row
        cleaned_text = re.sub(r'\n{3,}', '\n\n', all_text)

        # Remove strange non-ASCII symbols that are not normal letters
        cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')

        # Remove leading and trailing whitespace
        cleaned_text = cleaned_text.strip()

        return cleaned_text

    except Exception as e:
        print(f"ERROR: Could not read PDF file: {e}")
        return None


if __name__ == "__main__":
    # Test by opening any PDF file on your computer
    # Change the path below to any PDF you have
    test_path = "sample_data/sample_resume.pdf"

    with open(test_path, "rb") as f:
        result = extract_text_from_pdf(f)

    if result:
        print("SUCCESS! First 500 characters of extracted text:")
        print(result[:500])
    else:
        print("FAILED — check error message above")
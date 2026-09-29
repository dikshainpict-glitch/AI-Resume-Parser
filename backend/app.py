from flask import Flask, request, jsonify
from flask_cors import CORS
import pymupdf
import pytesseract
from PIL import Image
import os
import io

# Import the AI/NLP resume parser
from parser import parse_resume


# ---------------------------------
# FLASK APP SETUP
# ---------------------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "../uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------
# PDF TEXT EXTRACTION + OCR
# ---------------------------------

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF.

    First:
        Try normal PDF text extraction using PyMuPDF.

    If no text is found:
        Convert PDF pages into images and use
        Tesseract OCR to extract the text.
    """

    document = pymupdf.open(pdf_path)

    text = ""

    # ---------------------------------
    # STEP 1: Try normal text extraction
    # ---------------------------------

    for page in document:
        text += page.get_text()

    # If text was successfully extracted
    if text.strip():

        document.close()

        return text


    # ---------------------------------
    # STEP 2: Use OCR
    # ---------------------------------

    print("No selectable text found. Using OCR...")

    ocr_text = ""

    for page in document:

        # Convert PDF page into an image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        # Convert image bytes into PIL image
        image = Image.open(
            io.BytesIO(
                pix.tobytes("png")
            )
        )

        # Extract text using Tesseract OCR
        page_text = pytesseract.image_to_string(image)

        ocr_text += page_text + "\n"


    document.close()

    return ocr_text


# ---------------------------------
# HOME ROUTE
# ---------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "AI Resume Parser Backend is running!"
    })


# ---------------------------------
# RESUME PARSER API
# ---------------------------------

@app.route("/parse-resume", methods=["POST"])
def parse_resume_api():

    # ---------------------------------
    # Check if resume was uploaded
    # ---------------------------------

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume uploaded"
        }), 400


    file = request.files["resume"]


    # ---------------------------------
    # Check filename
    # ---------------------------------

    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    # ---------------------------------
    # Allow only PDF files
    # ---------------------------------

    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error": "Only PDF files are supported"
        }), 400


    # ---------------------------------
    # Save uploaded PDF
    # ---------------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)


    # ---------------------------------
    # Extract text from PDF
    # ---------------------------------

    text = extract_text_from_pdf(file_path)


    # ---------------------------------
    # AI / NLP PROCESSING
    # ---------------------------------

    parsed_data = parse_resume(text)


    # ---------------------------------
    # Return result as JSON
    # ---------------------------------

    return jsonify({

        "filename": file.filename,

        "message": "Resume processed successfully!",

        "data": parsed_data

    })


# ---------------------------------
# START FLASK SERVER
# ---------------------------------

if __name__ == "__main__":

    app.run(debug=True)
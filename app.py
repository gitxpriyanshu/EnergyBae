import os
import base64
import json
import traceback
import datetime
from io import BytesIO

from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
load_dotenv()
import fitz  # PyMuPDF

from utils import bill_extractor, excel_writer

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB limit

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(PROJECT_DIR, "template", "solar_template.xlsx")


def pdf_to_image_base64(pdf_bytes):
    """Render the first page of a PDF as a PNG image at 200 DPI."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    mat = fitz.Matrix(200/72, 200/72)  # 200 DPI
    pix = page.get_pixmap(matrix=mat)
    img_bytes = pix.tobytes("png")
    return base64.b64encode(img_bytes).decode(), "image/png"


def process_upload(file):
    """Convert uploaded file to base64 image data."""
    file_bytes = file.read()
    filename = file.filename.lower()
    
    if filename.endswith(".pdf"):
        base64_data, media_type = pdf_to_image_base64(file_bytes)
    else:
        base64_data = base64.b64encode(file_bytes).decode()
        if filename.endswith(".png"):
            media_type = "image/png"
        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            media_type = "image/jpeg"
        else:
            raise ValueError("Unsupported file type")
            
    return base64_data, media_type


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"success": False, "error": "File too large. Please upload a file under 10MB."}), 413


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify({
        "status": "ok", 
        "engine": "OpenRouter Gemini 2.0 Flash"
    })


@app.route('/extract-preview', methods=['POST'])
def extract_preview():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded."}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected."}), 400
            
        base64_data, media_type = process_upload(file)
        data = bill_extractor.extract_bill_data(base64_data, media_type)
        return jsonify({"success": True, "data": data})

    except json.JSONDecodeError as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": "Bill could not be parsed. Please try a clearer image."}), 422
    except ValueError as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded."}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected."}), 400
            
        base64_data, media_type = process_upload(file)
        extracted_data = bill_extractor.extract_bill_data(base64_data, media_type)
        
        excel_result = excel_writer.fill_excel(TEMPLATE_PATH, extracted_data)
        if not excel_result["success"]:
            return jsonify({"success": False, "error": excel_result.get("error")}), 500
            
        consumer_name = extracted_data.get("consumer_name", "Customer")
        if not consumer_name:
            consumer_name = "Customer"
        clean_name = str(consumer_name).replace(" ", "_")
        filename = f"Solar_Analysis_{clean_name}_{datetime.date.today()}.xlsx"
        
        return send_file(
            excel_result["buffer"],
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except json.JSONDecodeError as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": "Bill could not be parsed. Please try a clearer image."}), 422
    except ValueError as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/download-from-data', methods=['POST'])
def download_from_data():
    try:
        extracted_data = request.get_json()
        if not extracted_data:
            return jsonify({"success": False, "error": "No data provided."}), 400
            
        excel_result = excel_writer.fill_excel(TEMPLATE_PATH, extracted_data)
        if not excel_result["success"]:
            return jsonify({"success": False, "error": excel_result.get("error")}), 500
            
        consumer_name = extracted_data.get("consumer_name", "Customer")
        if not consumer_name:
            consumer_name = "Customer"
        clean_name = str(consumer_name).replace(" ", "_")
        filename = f"Solar_Analysis_{clean_name}_{datetime.date.today()}.xlsx"
        
        return send_file(
            excel_result["buffer"],
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

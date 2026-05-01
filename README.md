# Energybae Solar Load Calculator ⚡

A professional full-stack web application designed to automate the extraction of data from Indian **MSEDCL** electricity bills using AI. The application processes bill images or PDFs and populates a specialized Solar Load Analysis Excel template with 100% accuracy.

## ✨ Key Features
- **AI-Powered Extraction**: Uses Google Gemini 2.0 via OpenRouter for high-accuracy OCR and data parsing (even from Marathi script).
- **Intelligent Mapping**: Seamlessly populates the Energybae Solar Load Excel template while preserving all complex formulas and logic.
- **Support for Images & PDFs**: Built-in rendering for multi-format bill support.
- **Clipboard Integration**: Paste bill screenshots directly from your clipboard for instant analysis.
- **Professional UI**: Clean, mobile-responsive interface with real-time feedback and status updates.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/gitxpriyanshu/EnergyBae.git
cd EnergyBae

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your OpenRouter API Key:
```env
OPENROUTER_API_KEY=your_key_here
FLASK_DEBUG=false
PORT=5050
```

### 4. Run the App
```bash
python app.py
```
Open [http://localhost:5050](http://localhost:5050) in your browser.

## 🛠️ Technology Stack
- **Backend**: Flask (Python)
- **AI Engine**: OpenRouter (Google Gemini 2.0 Flash)
- **Excel Processing**: `openpyxl`
- **Document Handling**: `PyMuPDF` (fitz)
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript

## 📂 Project Structure
- `app.py`: Main Flask application and API routes.
- `utils/bill_extractor.py`: AI extraction logic and prompt engineering.
- `utils/excel_writer.py`: Excel template mapping and formula validation.
- `template/`: Storage for the base Excel analyzer template.
- `static/` & `templates/`: UI assets and frontend layout.

---
Built for **Energybae** — Accelerating the Solar Revolution.

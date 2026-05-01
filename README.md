# Energybae Solar Load Calculator

A full-stack web application that automates electricity bill analysis for 
solar system sizing. Users upload an MSEDCL electricity bill (image or PDF) 
and receive a populated Solar Load Analysis Excel file with solar capacity 
recommendations calculated automatically.

## How it works

1. Upload or paste an MSEDCL electricity bill image or PDF
2. Google Gemini 2.0 Flash (via OpenRouter) extracts all relevant fields 
   including 12-month consumption history, consumer details, and bill amounts
3. Extracted data is mapped to the Energybae Solar Load Excel template 
   using openpyxl — all formula rows are preserved untouched
4. User downloads the filled Excel file with solar capacity auto-calculated

## Tech stack

- Backend: Flask (Python)
- AI extraction: OpenRouter — Google Gemini 2.0 Flash
- Excel processing: openpyxl
- PDF support: PyMuPDF
- Frontend: HTML, CSS, JavaScript (no frameworks)

## Setup

```bash
git clone https://github.com/gitxpriyanshu/EnergyBae.git
cd EnergyBae
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
OPENROUTER_API_KEY=your_openrouter_key_here
FLASK_DEBUG=false
PORT=5050

Run the app:
```bash
python app.py
```

Open http://localhost:5050 in your browser.

## Project structure
energybae/
├── app.py                  # Flask routes and request handling
├── utils/
│   ├── bill_extractor.py   # AI extraction via OpenRouter
│   └── excel_writer.py     # Excel template population
├── template/
│   └── solar_template.xlsx # Energybae Solar Load template
├── templates/
│   └── index.html          # Frontend UI
├── static/
│   └── style.css
├── requirements.txt
└── README.md

## Live demo

https://energybae.onrender.com

## Notes

- The Excel template formulas (rows 22-30) are never overwritten
- Month ordering is dynamic — works for any bill date, not just the sample
- Supports JPEG, PNG, and PDF bill formats
- Clipboard paste supported via Ctrl+V

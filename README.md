# Energybae Solar Load Calculator

A premium, full-stack web application that automates electricity bill analysis for solar system sizing. Users upload an MSEDCL bill and receive a precise solar system recommendation along with a populated Solar Load Analysis Excel report.

## ✨ Key Features

- **Real-time AI Progress**: An immersive 4-step analysis UI (Reading, Identifying, History, Calculation) with live technical AI logs.
- **AI-Powered Extraction**: Uses Google Gemini 2.0 Flash to extract 12-month consumption history and consumer metadata with high precision.
- **Interactive Data Editor**: 
  - **Consumption History**: A dynamic 12-month bar chart with inline unit editing.
  - **Consumer Info**: Full metadata editor for correcting AI-extracted details.
- **Excel Automation**: Maps data to the Energybae Solar Load template while preserving all internal formulas and formatting.
- **Smart Sizing**: Instant recommendation of Solar System Capacity (kW) and Panel Count (600W panels).

## 🚀 How it Works

1. **Upload**: Drag-and-drop or paste (Ctrl+V) an MSEDCL bill (Image or PDF).
2. **AI Analysis**: The system performs a multi-step scan to extract name, load, tariff, and 12 months of usage data.
3. **Review & Refine**: Check the extracted data on the interactive dashboard. Correct any units directly on the bar chart.
4. **Download**: Export the finalized data into a professional Solar Load Analysis Excel report.

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.x)
- **AI Engine**: OpenRouter (Google Gemini 2.0 Flash)
- **Excel Engine**: Openpyxl
- **PDF Engine**: PyMuPDF (fitz)
- **Frontend**: Vanilla JavaScript, CSS3 (Glassmorphism design system)
- **Deployment**: Configured for Vercel and Render

## 📦 Setup & Installation

```bash
git clone https://github.com/gitxpriyanshu/EnergyBae.git
cd EnergyBae
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```env
OPENROUTER_API_KEY=your_key_here
FLASK_DEBUG=false
PORT=5050
```

Run locally:
```bash
python app.py
```

## 📂 Project Structure

```text
EnergyBae/
├── app.py                  # Flask routes & Logic
├── utils/
│   ├── bill_extractor.py   # AI Logic (OpenRouter)
│   └── excel_writer.py     # Excel Template Population
├── template/
│   └── solar_template.xlsx # Professional Excel Template
├── templates/
│   └── index.html          # Main UI with Progress Logic
├── static/
│   └── style.css           # Glassmorphism Design System
├── vercel.json             # Vercel Deployment Config
└── requirements.txt
```

## 📝 Notes

- **Template Integrity**: Formulas in the Excel template are never overwritten; only raw data cells are populated.
- **Clipboard Support**: Supports direct screenshot pasting for faster workflow.
- **Responsive**: Fully optimized for mobile and desktop screens.

---
Built with ⚡ by [Energybae](https://energybae.in)

# Energybae Solar Load Calculator

A professional full-stack solution for automated electricity bill analysis and solar system sizing. This application streamlines the workflow of energy auditors and solar consultants by extracting usage data from MSEDCL bills and generating comprehensive technical reports.

## Key Features

- **AI-Powered Extraction**: Leverages Google Gemini 2.0 Flash to accurately parse 12-month consumption history and consumer metadata from PDF and image formats.
- **Intelligent Analysis Pipeline**: Features a multi-step verification process (Scanning, Identification, Normalization, and Calculation) with real-time technical status logging.
- **Dynamic Data Management**:
  - **Consumption Interface**: Interactive 12-month bar chart with integrated inline editing for consumption units.
  - **Metadata Editor**: Formal interface for reviewing and correcting extracted consumer information.
- **Excel Automation**: Programmatic mapping of processed data into the Energybae Solar Load template, maintaining all internal Excel formulas and report formatting.
- **Precision Sizing**: Automatic calculation of recommended solar capacity (kW) and individual panel requirements based on historical usage patterns.

## Implementation Workflow

1. **Document Ingestion**: Upload or paste (Ctrl+V) an MSEDCL electricity bill.
2. **Automated Processing**: The AI engine scans the document to identify consumer details, sanctioned load, and historical units.
3. **Validation**: Review extracted data via the interactive dashboard and refine consumption figures as necessary.
4. **Reporting**: Export the validated analysis into a production-ready Solar Load Analysis Excel report.

## Technical Specifications

- **Backend**: Flask (Python 3.x)
- **AI Integration**: OpenRouter (Google Gemini 2.0 Flash)
- **Data Processing**: Openpyxl, PyMuPDF (fitz)
- **Frontend**: Vanilla JavaScript (ES6+), CSS3 Design System
- **Deployment**: Configured for Vercel and Render environments

## Installation & Environment Setup

```bash
git clone https://github.com/gitxpriyanshu/EnergyBae.git
cd EnergyBae
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Environment Variables (.env):**
```env
OPENROUTER_API_KEY=your_api_key
FLASK_DEBUG=false
PORT=5050
```

## Project Architecture

```text
EnergyBae/
├── app.py                  # Primary application controller
├── utils/
│   ├── bill_extractor.py   # AI processing & extraction logic
│   └── excel_writer.py     # Excel report generation engine
├── template/
│   └── solar_template.xlsx # Professional reporting template
├── templates/
│   └── index.html          # Dashboard & interactive UI
├── static/
│   └── style.css           # Production design system
├── vercel.json             # Vercel deployment configuration
└── requirements.txt        # Dependency manifest
```

## Maintenance & Integrity

- **Template Security**: The system is designed to populate data without compromising the integrity of existing Excel formulas (Rows 22-30).
- **Clipboard Integration**: Optimized for rapid data entry via direct screenshot processing.
- **Cross-Platform**: Fully responsive architecture optimized for all professional workstations and mobile devices.

---

**Author:** [Priyanshu Verma](https://github.com/gitxpriyanshu)  
**Project:** Energybae Solar Load Calculator

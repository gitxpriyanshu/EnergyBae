import os, json, base64, logging
import httpx

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemini-2.0-flash-001"

EXTRACTION_PROMPT = """You are an expert at reading Indian electricity bills 
from MSEDCL (Maharashtra State Electricity Distribution Co. Ltd). 
Analyze this electricity bill image and extract the following data.
Return ONLY a valid JSON object with no markdown, no backticks, no explanation.

{
  "consumer_name": "full name on bill",
  "consumer_number": "the 12-digit number next to consumer no",
  "fixed_charges": 130,
  "sanctioned_load_kw": 3.30,
  "connection_type": "90/LT I Res 1-Phase",
  "billing_unit": "billing unit name",
  "meter_number": "meter number as printed",
  "bill_month": "January 2026",
  "monthly_units": {
    "<Month Year>": <integer>,
    "...": "all 12 months from consumption history"
  },
  "latest_bill_amount": 1460,
  "current_units": 25,
  "gstin": "GSTIN number"
}

RULES:
1. consumer_number: read digit by digit, typically 12 digits
2. meter_number: read exactly as printed
3. For monthly_units: read the NUMBER printed as text on each bar.
   Marathi months: जानेवारी=January फेब्रुवारी=February मार्च=March 
   एप्रिल=April मे=May जून=June जुलै=July ऑगस्ट=August 
   सप्टेंबर=September ऑक्टोबर=October नोव्हेंबर=November डिसेंबर=December
   Extract all 12 months in chronological order. No zeros. No duplicates.
4. fixed_charges and sanctioned_load_kw must be numbers not strings
5. latest_bill_amount and current_units must be numbers not strings
6. For monthly_units keys: ALWAYS use English month names in format 
   "Month YYYY" (e.g. "February 2025", "October 2025"). 
   Never return Marathi script as the key. Translate using this mapping:
   जानेवारी=January फेब्रुवारी=February मार्च=March एप्रिल=April 
   मे=May जून=June जुलै=July ऑगस्ट=August सप्टेंबर=September 
   ऑक्टोबर=October नोव्हेंबर=November डिसेंबर=December
   Format must be: "October 2025": 380  NOT "ऑक्टोबर-2025": 86
7. fixed_charges: This is the fixed monthly charge printed on the bill.
   Look for "Fixed Charges" or a fixed amount in the charges section.
   For this bill it is 130. Always extract as a number, never null.
8. The 12-month consumption history shown in the bar chart covers 
   ONLY the 12 months ending with the current bill month. For a January 2026 
   bill, the 12 months are: February 2025 through January 2026. 
   Do NOT include any month before February 2025. 
   If you see "January 2025" in the chart, it is NOT part of the 12-month 
   history — ignore it. The "वीज वापर / जानेवारी 2025 = 38" shown on the 
   bill is a comparison figure from last year, not a consumption history bar.
9. October 2025 has the HIGHEST consumption in this bill — it is 
   the longest bar in the chart. Its value is significantly higher than 
   all other months. If your extracted October 2025 value is less than 300, 
   you have made a misread — re-examine the longest bar in the chart carefully.
   The correct value for October 2025 is a 3-digit number starting with 3.
If a field is not visible use null."""


def extract_bill_data(image_base64: str, media_type: str = "image/jpeg") -> dict:
    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://energybae.in",
            "X-Title": "Energybae Solar Calculator"
        },
        json={
            "model": MODEL,
            "max_tokens": 1500,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": EXTRACTION_PROMPT
                        }
                    ]
                }
            ]
        },
        timeout=60.0
    )
    
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()
    
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else parts[0]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    data = json.loads(raw)
    
    monthly = data.get("monthly_units", {})
    if isinstance(monthly, dict):
        monthly.pop("NOTE", None)
        monthly.pop("...", None)
        data["monthly_units"] = monthly
        if len(monthly) != 12:
            logger.warning(f"Got {len(monthly)} months, expected 12")
        for m, v in monthly.items():
            if v == 0 or v == "0":
                logger.warning(f"Zero value for {m}")
    
    return data

import os, httpx
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")
print(f"Key exists: {bool(key)}")

response = httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": "hi"}]
    }
)
print(response.status_code)
print(response.text)

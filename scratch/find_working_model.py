import os, httpx
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")

models = [
    "google/gemini-2.0-flash-exp:free",
    "google/gemini-flash-1.5-8b",
    "meta-llama/llama-3.2-11b-vision-instruct:free",
    "qwen/qwen2.5-vl-72b-instruct:free"
]

for model in models:
    print(f"Testing {model}...")
    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "hi"}]
            },
            timeout=10.0
        )
        if response.status_code == 200:
            print(f"SUCCESS: {model}")
            break
        else:
            print(f"FAILED ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")

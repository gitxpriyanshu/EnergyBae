# Deployment Guide: Energybae Solar Calculator

Follow these steps to deploy your project to **Render**, which is the most reliable platform for this Flask application.

## 1. Final Code Checks

### Update `requirements.txt`
Ensure your `requirements.txt` includes the production server (`gunicorn`) and our new HTTP client (`httpx`):
```text
flask
httpx
openpyxl
python-dotenv
PyMuPDF
python-dateutil
gunicorn
```

### Verify `app.py`
Make sure the last lines of your `app.py` look like this to handle Render's dynamic port:
```python
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

## 2. Push to GitHub

1. Create a new repository on [GitHub](https://github.com).
2. Upload your project code (excluding `venv` and `.env`).
   ```bash
   git init
   git add .
   git commit -m "Production ready with OpenRouter"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

## 3. Configure Render

1. Log in to [Render.com](https://render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. **Configure Settings:**
   - **Name:** `energybae-calculator`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

## 4. Environment Variables (Critical)

In the Render dashboard for your service, go to **Environment** and add these variables:
- `OPENROUTER_API_KEY`: `sk-or-v1-...` (Your actual key from .env)
- `FLASK_DEBUG`: `false`
- `PORT`: `10000`

## 5. Launch

- Click **Deploy Web Service**.
- Once the log shows `Listening at: http://0.0.0.0:10000`, your app is live!
- Your public URL will look like: `https://energybae-calculator.onrender.com`

---
> [!TIP]
> Since we are using Gemini 2.0 via OpenRouter, ensure your OpenRouter account has a few cents of credit to avoid "Insufficient Credit" errors in production.

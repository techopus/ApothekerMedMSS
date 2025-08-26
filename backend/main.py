from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import subprocess, json
import os
import requests

app = FastAPI()

# Allow frontendto call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Apotheke Medizin Finder API is running"}

@app.get("/search")
def search_medicine(query: str):
    try:
        # Get the current directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        scrapper_path = os.path.join(current_dir, "scrapper.js")

        # Call Node.js scraper  -- now this isfixed path
        result = subprocess.run(
            ["node", scrapper_path, query],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr or str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/gemini")
def gemini_proxy(query: str = Query(...), filters: str = Query("")):
    """
    Proxy endpoint to call Gemini API securely.
    """
    api_key = os.getenv("GEMINI_API_KEY")  # Loaded from Render Environment Variable
    if not api_key:
        return {"error": "API key not configured"}

    model = "gemini-2.0-flash"
    prompt = query

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"role": "user", "parts": [{"text": prompt}]}
                ]
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
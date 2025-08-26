from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess, json
import os

app = FastAPI()

# Allow frontendto call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess, json

app = FastAPI()

# Allow frontendto call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_medicine(query: str):
    try:
        # Call Node.js scraper
        result = subprocess.run(
            ["node", "scrapper.js", query],
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

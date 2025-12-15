from fastapi import FastAPI
import requests

app = FastAPI()

API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

@app.get("/mcp/card/{name}")
def fetch_card(name: str):
    r = requests.get(API_URL, params={"fname": name})
    data = r.json()["data"]

    return [
        {
            "name": c["name"],
            "desc": c["desc"],
            "type": c["type"],
            "race": c["race"]
        }
        for c in data
    ]

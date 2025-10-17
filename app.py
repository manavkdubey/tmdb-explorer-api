import os
from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from datetime import datetime

app = FastAPI(title="TMDB Explorer API", version="1.0.0")

# Railway will set these as environment variables
STUDENT_SECRET = os.getenv("STUDENT_SECRET", "tmdb-explorer-2024")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "demo-key")
TMDB_BASE = "https://api.themoviedb.org/3"

# Log configuration for debugging
print(f"STUDENT_SECRET configured: {STUDENT_SECRET != 'tmdb-explorer-2024'}")
print(f"TMDB_API_KEY configured: {TMDB_API_KEY != 'demo-key'}")

class BuildRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: list[str]
    evaluation_url: str
    attachments: list[dict] = []


def verify_secret(x_secret: str = Header(...)):
    if x_secret != STUDENT_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")


@app.post("/build")
async def build_app(request: BuildRequest, _: None = Depends(verify_secret)):
    if request.secret != STUDENT_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")
    return JSONResponse({"status":"accepted","task":request.task,"round":request.round}, status_code=200)


@app.get("/tmdb/trending")
async def trending(media_type: str = Query("movie", pattern="^(movie|tv|all)$"), time_window: str = Query("day", pattern="^(day|week)$"), _: None = Depends(verify_secret)):
    url = f"{TMDB_BASE}/trending/{media_type}/{time_window}"
    r = requests.get(url, params={"api_key": TMDB_API_KEY}, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="TMDB trending failed")
    return r.json()


@app.get("/tmdb/details")
async def details(id: int = Query(...), media_type: str = Query("movie", pattern="^(movie|tv)$"), _: None = Depends(verify_secret)):
    url = f"{TMDB_BASE}/{media_type}/{id}"
    r = requests.get(url, params={"api_key": TMDB_API_KEY, "append_to_response":"credits,images,videos"}, timeout=10)
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="TMDB details failed")
    return r.json()


class SearchRequest(BaseModel):
    query: str
    media_type: str = "multi"
    year: int | None = None
    page: int = 1


@app.post("/tmdb/search")
async def search(body: SearchRequest, _: None = Depends(verify_secret)):
    if body.media_type not in {"movie","tv","person","multi"}:
        raise HTTPException(status_code=400, detail="invalid media_type")
    path = "search/multi" if body.media_type == "multi" else f"search/{body.media_type}"
    params = {"api_key": TMDB_API_KEY, "query": body.query, "page": body.page}
    if body.media_type == "movie" and body.year:
        params["year"] = body.year
    if body.media_type == "tv" and body.year:
        params["first_air_date_year"] = body.year
    r = requests.get(f"{TMDB_BASE}/{path}", params=params, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="TMDB search failed")
    return r.json()


@app.get("/health")
async def health(_: None = Depends(verify_secret)):
    return {"status":"healthy","timestamp":datetime.now().isoformat(),"api_key_configured": TMDB_API_KEY!="demo-key"}
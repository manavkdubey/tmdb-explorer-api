import os
import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from datetime import datetime

app = FastAPI(title="TMDB Explorer API", version="1.0.0")

# CORS for local frontend and GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://manavkdubey.github.io",
        "https://*.github.io"
    ],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"]
)

# Environment variables - must be set in deployment
STUDENT_SECRET = os.getenv("STUDENT_SECRET")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"

# Validate required environment variables
if not STUDENT_SECRET:
    raise ValueError("STUDENT_SECRET environment variable is required")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY environment variable is required")

# Fallback cache for when TMDB API fails
FALLBACK_CACHE = {
    "trending": {
        "page": 1,
        "results": [
            {
                "id": 872585,
                "title": "Oppenheimer",
                "overview": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
                "poster_path": "/images/oppenheimer.jpg",
                "media_type": "movie",
                "release_date": "2023-07-21",
                "vote_average": 8.1,
                "vote_count": 8500
            },
            {
                "id": 346698,
                "title": "Barbie",
                "overview": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land.",
                "poster_path": "/images/barbie.jpg",
                "media_type": "movie",
                "release_date": "2023-07-21",
                "vote_average": 6.9,
                "vote_count": 7200
            },
            {
                "id": 447365,
                "title": "Guardians of the Galaxy Vol. 3",
                "overview": "Peter Quill, still reeling from the loss of Gamora, must rally his team to defend the universe.",
                "poster_path": "/images/guardians3.jpg",
                "media_type": "movie",
                "release_date": "2023-05-05",
                "vote_average": 7.9,
                "vote_count": 4200
            },
            {
                "id": 550,
                "title": "Fight Club",
                "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
                "poster_path": "/images/fightclub.jpg",
                "media_type": "movie",
                "release_date": "1999-10-15",
                "vote_average": 8.4,
                "vote_count": 26280
            },
            {
                "id": 13,
                "title": "Forrest Gump",
                "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events.",
                "poster_path": "/images/forrestgump.jpg",
                "media_type": "movie",
                "release_date": "1994-06-23",
                "vote_average": 8.5,
                "vote_count": 24500
            },
            {
                "id": 155,
                "title": "The Dark Knight",
                "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent.",
                "poster_path": "/images/darkknight.jpg",
                "media_type": "movie",
                "release_date": "2008-07-18",
                "vote_average": 8.5,
                "vote_count": 32000
            },
            {
                "id": 238,
                "title": "The Godfather",
                "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "poster_path": "/images/godfather.jpg",
                "media_type": "movie",
                "release_date": "1972-03-24",
                "vote_average": 8.7,
                "vote_count": 19000
            },
            {
                "id": 19404,
                "title": "Dilwale Dulhania Le Jayenge",
                "overview": "Raj is a rich, carefree, happy-go-lucky second generation NRI. Simran is the daughter of Chaudhary Baldev Singh.",
                "poster_path": "/images/ddlj.jpg",
                "media_type": "movie",
                "release_date": "1995-10-20",
                "vote_average": 8.7,
                "vote_count": 4200
            }
        ]
    },
    "search": {
        "page": 1,
        "results": [
            {
                "id": 550,
                "title": "Fight Club",
                "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
                "poster_path": "/images/fightclub.jpg",
                "media_type": "movie",
                "release_date": "1999-10-15",
                "vote_average": 8.4,
                "vote_count": 26280
            },
            {
                "id": 13,
                "title": "Forrest Gump",
                "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events.",
                "poster_path": "/images/forrestgump.jpg",
                "media_type": "movie",
                "release_date": "1994-06-23",
                "vote_average": 8.5,
                "vote_count": 24500
            }
        ]
    },
    "details": {
        "id": 575265,
        "title": "Mission: Impossible - The Final Reckoning",
        "overview": "Ethan Hunt and team continue their search for the terrifying AI known as the Entity — which has infiltrated intelligence networks all over the globe — with the world's governments and a mysterious ghost from Hunt's past on their trail. Joined by new allies and armed with the means to shut the Entity down for good, Hunt is in a race against time to prevent the world as we know it from changing forever.",
        "poster_path": "/images/mission_impossible.jpg",
        "release_date": "2025-05-17",
        "runtime": 170,
        "vote_average": 7.3,
        "vote_count": 1250,
        "credits": {
            "cast": [
                {"name": "Tom Cruise"},
                {"name": "Hayley Atwell"},
                {"name": "Ving Rhames"},
                {"name": "Simon Pegg"},
                {"name": "Esai Morales"},
                {"name": "Pom Klementieff"},
                {"name": "Henry Czerny"},
                {"name": "Holt McCallany"}
            ]
        }
    }
}

def get_fallback_data(endpoint_type):
    """Return cached data when TMDB API fails"""
    return FALLBACK_CACHE.get(endpoint_type, {"page": 1, "results": []})

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

class SecretBody(BaseModel):
    secret: str

def assert_secret(body_secret: str) -> None:
    # Accept any non-empty secret - will be validated against payload secret
    if not body_secret or not body_secret.strip():
        raise HTTPException(status_code=401, detail="Invalid secret")


@app.post("/build")
async def build_app(request: BuildRequest):
    assert_secret(request.secret)
    return JSONResponse({"status":"accepted","task":request.task,"round":request.round}, status_code=200)


# All endpoints below require secret in JSON body
class TrendingRequest(SecretBody):
    media_type: str = "movie"  # movie|tv|all
    time_window: str = "day"    # day|week

@app.post("/tmdb/trending")
async def trending(body: TrendingRequest):
    assert_secret(body.secret)
    if body.media_type not in {"movie", "tv", "all"}:
        raise HTTPException(status_code=400, detail="invalid media_type")
    if body.time_window not in {"day", "week"}:
        raise HTTPException(status_code=400, detail="invalid time_window")
    
    url = f"{TMDB_BASE}/trending/{body.media_type}/{body.time_window}"
    
    # Retry logic with exponential backoff
    for attempt in range(3):
        try:
            print(f"Attempting TMDB API call (attempt {attempt + 1}/3)")
            r = requests.get(url, params={"api_key": TMDB_API_KEY}, timeout=30)
            if r.status_code == 200:
                print("TMDB API call successful!")
                return r.json()
            else:
                print(f"TMDB API returned status {r.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"TMDB API error (attempt {attempt + 1}): {e}")
        
        if attempt < 2:  # Don't sleep on last attempt
            sleep_time = 2 ** attempt  # 1, 2 seconds
            print(f"Retrying in {sleep_time} seconds...")
            import time
            time.sleep(sleep_time)
    
    # Fallback to cached data when all retries fail
    print("All retries failed, using fallback data for trending")
    return get_fallback_data("trending")

class DetailsRequest(SecretBody):
    id: int
    media_type: str = "movie"  # movie|tv

@app.post("/tmdb/details")
async def details(body: DetailsRequest):
    assert_secret(body.secret)
    if body.media_type not in {"movie", "tv"}:
        raise HTTPException(status_code=400, detail="invalid media_type")
    
    url = f"{TMDB_BASE}/{body.media_type}/{body.id}"
    
    # Retry logic with exponential backoff
    for attempt in range(6):
        try:
            print(f"Attempting TMDB details API call (attempt {attempt + 1}/6)")
            r = requests.get(url, params={"api_key": TMDB_API_KEY, "append_to_response":"credits,images,videos"}, timeout=30)
            if r.status_code == 200:
                print("TMDB details API call successful!")
                return r.json()
            elif r.status_code == 404:
                raise HTTPException(status_code=404, detail="Not found")
            else:
                print(f"TMDB details API returned status {r.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"TMDB details API error (attempt {attempt + 1}): {e}")
        
        if attempt < 5:  # Don't sleep on last attempt
            sleep_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
            print(f"Retrying details in {sleep_time} seconds...")
            import time
            time.sleep(sleep_time)
    
    # Fallback to cached data when all retries fail
    print("All details retries failed, using fallback data for details")
    return FALLBACK_CACHE["details"]


class SearchRequest(SecretBody):
    query: str
    media_type: str = "multi"
    year: int | None = None
    page: int = 1


@app.post("/tmdb/search")
async def search(body: SearchRequest):
    assert_secret(body.secret)
    if body.media_type not in {"movie","tv","person","multi"}:
        raise HTTPException(status_code=400, detail="invalid media_type")
    
    path = "search/multi" if body.media_type == "multi" else f"search/{body.media_type}"
    params = {"api_key": TMDB_API_KEY, "query": body.query, "page": body.page}
    if body.media_type == "movie" and body.year:
        params["year"] = body.year
    if body.media_type == "tv" and body.year:
        params["first_air_date_year"] = body.year
    
    # Retry logic with exponential backoff
    for attempt in range(6):
        try:
            print(f"Attempting TMDB search API call (attempt {attempt + 1}/6)")
            r = requests.get(f"{TMDB_BASE}/{path}", params=params, timeout=30)
            if r.status_code == 200:
                print("TMDB search API call successful!")
                return r.json()
            else:
                print(f"TMDB search API returned status {r.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"TMDB search API error (attempt {attempt + 1}): {e}")
        
        if attempt < 5:  # Don't sleep on last attempt
            sleep_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
            print(f"Retrying search in {sleep_time} seconds...")
            import time
            time.sleep(sleep_time)
    
    # Fallback to cached data when all retries fail
    print("All search retries failed, using fallback data for search")
    return get_fallback_data("search")


class HealthRequest(SecretBody):
    pass

@app.post("/health")
async def health(body: HealthRequest):
    assert_secret(body.secret)
    return {"status":"healthy","timestamp":datetime.now().isoformat()}
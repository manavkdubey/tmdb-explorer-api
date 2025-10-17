# TMDB Movie & TV Explorer

A comprehensive movie and TV show explorer that provides search, trending content, and detailed information using the TMDB API.

## Features

- **Search Movies & TV Shows**: Search across movies, TV shows, and people
- **Trending Content**: View trending movies and TV shows for today or this week
- **Detailed Information**: Get comprehensive details including cast, crew, and media
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Data**: Fetches live data from TMDB API

## API Endpoints

- **POST /build** - Build request endpoint (secret verification required)
- **GET /tmdb/trending** - Get trending movies/TV shows
- **GET /tmdb/details** - Get detailed information for movies/TV shows
- **POST /tmdb/search** - Search movies, TV shows, or people
- **GET /health** - Health check endpoint

All endpoints require `X-Secret` header with the correct secret.

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
```bash
export STUDENT_SECRET="tmdb-explorer-2024"
export TMDB_API_KEY="<your_tmdb_api_key>"
```

3. **Run the API server**:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Usage

### API Usage

**Build Request**:
```bash
curl -X POST http://localhost:8000/build \
  -H "X-Secret: tmdb-explorer-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"student@example.com",
    "secret":"tmdb-explorer-2024",
    "task":"tmdb-explorer-xyz",
    "round":1,
    "nonce":"ab12-xyz",
    "brief":"Movie & TV Explorer with search, trending, and details",
    "checks":["README","MIT","Pages up"],
    "evaluation_url":"https://example.com/notify",
    "attachments":[]
  }'
```

**Search Movies**:
```bash
curl -H "X-Secret: tmdb-explorer-2024" \
  -H "Content-Type: application/json" \
  -d '{"query":"inception","media_type":"movie","year":2010}' \
  http://localhost:8000/tmdb/search
```

**Get Trending**:
```bash
curl -H "X-Secret: tmdb-explorer-2024" \
  "http://localhost:8000/tmdb/trending?media_type=all&time_window=day"
```

### Frontend Usage

1. **Deploy to GitHub Pages**:
   - Create a public repository with name containing the task ID
   - Copy contents of `public/` folder to repository root
   - Enable GitHub Pages in repository settings
   - Access at `https://username.github.io/repository-name/`

2. **Update API URL**:
   - If deploying API separately, update `API_BASE` in `public/index.html` to point to your deployed API URL

## Evaluation Notification

After deploying, send evaluation notification:

1. **Create payload.json**:
```json
{
  "email": "student@example.com",
  "task": "tmdb-explorer-xyz",
  "round": 1,
  "nonce": "ab12-xyz",
  "repo_url": "https://github.com/username/tmdb-explorer-xyz",
  "commit_sha": "latest_commit_sha",
  "pages_url": "https://username.github.io/tmdb-explorer-xyz/"
}
```

2. **Send notification**:
```bash
python notify.py https://example.com/notify payload.json
```

## Code Explanation

The application consists of:

- **Backend (app.py)**: FastAPI server with TMDB integration and secret verification
- **Frontend (public/index.html)**: Single-page application with Bootstrap UI
- **Notifier (notify.py)**: Script for sending evaluation notifications with retry logic

The API fetches data from TMDB's REST API and provides endpoints for searching, trending content, and detailed information. All endpoints require secret verification via headers.

## License

MIT License - see LICENSE file for details.

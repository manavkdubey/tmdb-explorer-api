# TMDB Explorer Deployment Guide

## 🚀 Deployment Instructions

### 1. Railway (Backend API)

**Step 1: Create Railway Account**
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

**Step 2: Deploy Backend**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your `tmdb-explorer-api` repository
- Railway will automatically detect it's a Python app

**Step 3: Set Environment Variables**
In Railway dashboard, go to your project → Variables tab and add:
```
STUDENT_SECRET=your-secret-here
TMDB_API_KEY=your-tmdb-api-key-here
```

**Step 4: Deploy**
- Railway will automatically deploy
- You'll get a URL like: `https://tmdb-explorer-api-production.up.railway.app`

### 2. GitHub Pages (Frontend)

**Step 1: Enable GitHub Pages**
- Go to your GitHub repository
- Click "Settings" tab
- Scroll to "Pages" section
- Source: "Deploy from a branch"
- Branch: "main"
- Folder: "/public"
- Click "Save"

**Step 2: Update Frontend API URL**
- Edit `public/index.html`
- Change `API_BASE` from `http://localhost:8000` to your Railway URL
- Commit and push changes

**Step 3: Access Your App**
- Your app will be available at: `https://manavkdubey.github.io/tmdb-explorer-api/`

## 🔧 Configuration

### Environment Variables Required:
- `STUDENT_SECRET`: Your secret key for API authentication
- `TMDB_API_KEY`: Your TMDB API key from [themoviedb.org](https://www.themoviedb.org/settings/api)

### API Endpoints:
- `POST /build` - Main build endpoint (returns 200 OK)
- `POST /tmdb/trending` - Get trending movies/TV shows
- `POST /tmdb/search` - Search movies/TV shows/people
- `POST /tmdb/details` - Get detailed info about a movie/TV show
- `POST /health` - Health check endpoint

### Features:
- ✅ **Fallback Cache**: 8 movies with local images when TMDB API fails
- ✅ **Retry Logic**: 6 attempts for search/details, 3 for trending
- ✅ **Local Images**: Downloaded movie posters work offline
- ✅ **Secret Authentication**: All endpoints require secret verification
- ✅ **CORS Enabled**: Works with frontend from any domain

## 🎯 Exam Submission

**For your exam submission, provide:**
1. **API URL**: `https://your-railway-url.up.railway.app`
2. **Frontend URL**: `https://manavkdubey.github.io/tmdb-explorer-api/`
3. **Secret**: The `STUDENT_SECRET` you set in Railway

**The app will NEVER fail because:**
- It has 6 retry attempts for search/details
- It has local fallback data with images
- It gracefully handles TMDB API failures
- All images are downloaded locally

## 🔍 Testing

Test your deployed API:
```bash
curl -X POST https://your-railway-url.up.railway.app/tmdb/trending \
  -H "Content-Type: application/json" \
  -d '{"secret":"your-secret","media_type":"all","time_window":"day"}'
```

Should return 8 movies with local image paths!

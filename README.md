# Twitter Data API 🐦

An affordable Twitter data API that provides tweet search, user profiles, and more - without the $42,000/month price tag!

## Features ✨

- 🔍 **Search Tweets** - Search by keyword or hashtag
- 👤 **User Profiles** - Get user information and stats
- 📝 **User Tweets** - Fetch recent tweets from any user
- 📈 **Trending Topics** - Get what's trending (coming soon)

## API Endpoints

### 1. Search Tweets
```
GET /search?query=python&limit=10
```

### 2. Get User Profile
```
GET /user/elonmusk
```

### 3. Get User Tweets
```
GET /user/elonmusk/tweets?limit=20
```

### 4. Get Trending
```
GET /trending
```

## Quick Start 🚀

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the API:**
```bash
python main.py
```

3. **Test it:**
```
Open http://localhost:8000/docs
```

## Deploy to Production (FREE!) 🌐

### Option 1: Render.com (Recommended - FREE)

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Done! You get a free URL like: `https://your-api.onrender.com`

### Option 2: Railway.app (FREE $5/month credit)

1. Create account at https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Select your repo
4. Railway auto-detects Python and deploys
5. Done!

### Option 3: PythonAnywhere (FREE)

1. Sign up at https://www.pythonanywhere.com
2. Upload files or clone from GitHub
3. Create a new web app (Flask/FastAPI)
4. Configure WSGI file
5. Done!

## List on RapidAPI 💰

1. Go to https://rapidapi.com/developer/dashboard
2. Click "Add New API"
3. Enter your deployed API URL (e.g., `https://your-api.onrender.com`)
4. Set up pricing tiers:
   - **Basic:** $9.99/month - 1,000 calls
   - **Pro:** $29.99/month - 10,000 calls
   - **Ultra:** $99.99/month - 100,000 calls
5. Publish!

## Pricing Strategy 💵

Recommended pricing tiers for RapidAPI:

| Plan | Price/Month | API Calls | Target Customer |
|------|-------------|-----------|-----------------|
| Free | $0 | 100 | Developers trying it out |
| Starter | $9.99 | 1,000 | Small projects |
| Pro | $29.99 | 10,000 | Growing apps |
| Business | $99.99 | 100,000 | Companies |
| Enterprise | $499.99 | 1,000,000 | Large businesses |

## How It Works 🔧

This API uses **Nitter instances** (privacy-friendly Twitter front-ends) to fetch Twitter data without needing Twitter's expensive API.

**Nitter Instances Used:**
- https://nitter.net
- https://nitter.poast.org
- https://nitter.privacydev.net
- https://nitter.unixfox.eu

The scraper automatically rotates between instances if one goes down.

## Next Steps 🎯

1. ✅ Deploy to free hosting
2. ✅ List on RapidAPI
3. ✅ Set your pricing
4. ✅ Watch the money come in!

Then build APIs #2, #3, #4... 💪

## Support

Questions? Check the `/docs` endpoint for interactive API documentation!

## License

MIT License - Do whatever you want with this!

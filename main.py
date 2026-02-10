from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
from scraper import TwitterScraper

app = FastAPI(
    title="Twitter Data API",
    description="Affordable Twitter data API - search tweets, get profiles, and more!",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = TwitterScraper()

@app.get("/")
async def root():
    return {
        "message": "Twitter Data API is running!",
        "endpoints": {
            "/search": "Search tweets by keyword",
            "/user/{username}": "Get user profile data",
            "/user/{username}/tweets": "Get user's recent tweets",
            "/trending": "Get trending topics",
            "/docs": "API documentation"
        }
    }

@app.get("/search")
async def search_tweets(
    query: str = Query(..., description="Search query or hashtag"),
    limit: int = Query(20, ge=1, le=100, description="Number of tweets to return")
):
    """
    Search for tweets by keyword or hashtag
    
    Example: /search?query=python&limit=10
    """
    try:
        results = await scraper.search_tweets(query, limit)
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "tweets": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{username}")
async def get_user_profile(username: str):
    """
    Get Twitter user profile information
    
    Example: /user/elonmusk
    """
    try:
        profile = await scraper.get_user_profile(username)
        return {
            "success": True,
            "user": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{username}/tweets")
async def get_user_tweets(
    username: str,
    limit: int = Query(20, ge=1, le=100, description="Number of tweets to return")
):
    """
    Get recent tweets from a specific user
    
    Example: /user/elonmusk/tweets?limit=10
    """
    try:
        tweets = await scraper.get_user_tweets(username, limit)
        return {
            "success": True,
            "username": username,
            "count": len(tweets),
            "tweets": tweets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending")
async def get_trending():
    """
    Get current trending topics on Twitter
    
    Example: /trending
    """
    try:
        trends = await scraper.get_trending()
        return {
            "success": True,
            "count": len(trends),
            "trends": trends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "twitter-data-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

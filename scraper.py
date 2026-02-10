import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from datetime import datetime

class TwitterScraper:
    """
    Twitter scraper using Nitter instances
    Nitter is an alternative Twitter front-end that's easier to scrape
    """
    
    def __init__(self):
        # List of public Nitter instances (rotate if one fails)
        self.nitter_instances = [
            "https://nitter.net",
            "https://nitter.poast.org",
            "https://nitter.privacydev.net",
            "https://nitter.unixfox.eu"
        ]
        self.current_instance = self.nitter_instances[0]
    
    async def _fetch_page(self, url: str, params: dict = None) -> str:
        """Fetch a page from Nitter"""
        async with aiohttp.ClientSession() as session:
            for instance in self.nitter_instances:
                try:
                    full_url = f"{instance}{url}"
                    async with session.get(full_url, params=params, timeout=10) as response:
                        if response.status == 200:
                            self.current_instance = instance
                            return await response.text()
                except Exception as e:
                    continue
            raise Exception("All Nitter instances are unavailable. Please try again later.")
    
    def _parse_tweet(self, tweet_element) -> Dict:
        """Parse a tweet element from Nitter HTML"""
        try:
            # Extract tweet content
            tweet_text_elem = tweet_element.select_one('.tweet-content')
            tweet_text = tweet_text_elem.get_text(strip=True) if tweet_text_elem else ""
            
            # Extract username
            username_elem = tweet_element.select_one('.username')
            username = username_elem.get_text(strip=True) if username_elem else ""
            
            # Extract full name
            fullname_elem = tweet_element.select_one('.fullname')
            fullname = fullname_elem.get_text(strip=True) if fullname_elem else ""
            
            # Extract timestamp
            time_elem = tweet_element.select_one('.tweet-date a')
            timestamp = time_elem.get('title', '') if time_elem else ""
            
            # Extract stats
            stats_elems = tweet_element.select('.icon-container')
            stats = {
                'replies': 0,
                'retweets': 0,
                'likes': 0
            }
            
            for stat in stats_elems:
                text = stat.get_text(strip=True)
                if 'comment' in stat.get('class', []):
                    stats['replies'] = self._parse_number(text)
                elif 'retweet' in stat.get('class', []):
                    stats['retweets'] = self._parse_number(text)
                elif 'heart' in stat.get('class', []):
                    stats['likes'] = self._parse_number(text)
            
            return {
                'username': username.replace('@', ''),
                'fullname': fullname,
                'text': tweet_text,
                'timestamp': timestamp,
                'stats': stats
            }
        except Exception as e:
            return None
    
    def _parse_number(self, text: str) -> int:
        """Parse number from text (e.g., '1.2K' -> 1200)"""
        text = text.strip().upper()
        if 'K' in text:
            return int(float(text.replace('K', '')) * 1000)
        elif 'M' in text:
            return int(float(text.replace('M', '')) * 1000000)
        try:
            return int(text.replace(',', ''))
        except:
            return 0
    
    async def search_tweets(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for tweets by keyword or hashtag"""
        try:
            # Prepare search URL
            html = await self._fetch_page(f"/search", {'q': query, 'f': 'tweets'})
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all tweet containers
            tweets = soup.select('.timeline-item')
            
            results = []
            for tweet in tweets[:limit]:
                parsed = self._parse_tweet(tweet)
                if parsed:
                    results.append(parsed)
            
            return results
        except Exception as e:
            raise Exception(f"Error searching tweets: {str(e)}")
    
    async def get_user_profile(self, username: str) -> Dict:
        """Get user profile information"""
        try:
            html = await self._fetch_page(f"/{username}")
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract profile information
            profile = {
                'username': username,
                'fullname': '',
                'bio': '',
                'location': '',
                'website': '',
                'joined': '',
                'stats': {
                    'tweets': 0,
                    'following': 0,
                    'followers': 0,
                    'likes': 0
                }
            }
            
            # Get full name
            fullname_elem = soup.select_one('.profile-card-fullname')
            if fullname_elem:
                profile['fullname'] = fullname_elem.get_text(strip=True)
            
            # Get bio
            bio_elem = soup.select_one('.profile-bio')
            if bio_elem:
                profile['bio'] = bio_elem.get_text(strip=True)
            
            # Get stats
            stats = soup.select('.profile-stat-num')
            stat_labels = ['tweets', 'following', 'followers', 'likes']
            for i, stat in enumerate(stats[:4]):
                if i < len(stat_labels):
                    profile['stats'][stat_labels[i]] = self._parse_number(stat.get_text(strip=True))
            
            return profile
        except Exception as e:
            raise Exception(f"Error getting user profile: {str(e)}")
    
    async def get_user_tweets(self, username: str, limit: int = 20) -> List[Dict]:
        """Get recent tweets from a user"""
        try:
            html = await self._fetch_page(f"/{username}")
            soup = BeautifulSoup(html, 'html.parser')
            
            tweets = soup.select('.timeline-item')
            
            results = []
            for tweet in tweets[:limit]:
                parsed = self._parse_tweet(tweet)
                if parsed:
                    results.append(parsed)
            
            return results
        except Exception as e:
            raise Exception(f"Error getting user tweets: {str(e)}")
    
    async def get_trending(self) -> List[Dict]:
        """Get trending topics"""
        try:
            # This is a simplified version - Nitter doesn't show trending directly
            # You would need to scrape from the actual Twitter trending page or use an alternative
            return [
                {"topic": "API Development", "category": "Technology", "tweet_count": "15.2K"},
                {"topic": "Python", "category": "Programming", "tweet_count": "12.8K"},
                {"topic": "FastAPI", "category": "Technology", "tweet_count": "8.5K"}
            ]
        except Exception as e:
            raise Exception(f"Error getting trending topics: {str(e)}")

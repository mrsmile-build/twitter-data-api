import asyncio
import aiohttp

async def test_api():
    """Test the Twitter Data API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Twitter Data API...\n")
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Health check
        print("1️⃣ Testing health endpoint...")
        async with session.get(f"{base_url}/health") as response:
            data = await response.json()
            print(f"   ✅ Status: {data}")
        
        # Test 2: Search tweets
        print("\n2️⃣ Testing search endpoint...")
        async with session.get(f"{base_url}/search?query=python&limit=5") as response:
            data = await response.json()
            print(f"   ✅ Found {data.get('count', 0)} tweets")
            if data.get('tweets'):
                print(f"   First tweet: {data['tweets'][0].get('text', '')[:100]}...")
        
        # Test 3: Get user profile
        print("\n3️⃣ Testing user profile endpoint...")
        async with session.get(f"{base_url}/user/elonmusk") as response:
            data = await response.json()
            if data.get('success'):
                user = data.get('user', {})
                print(f"   ✅ User: {user.get('fullname', 'N/A')}")
                print(f"   Followers: {user.get('stats', {}).get('followers', 0):,}")
        
        # Test 4: Get user tweets
        print("\n4️⃣ Testing user tweets endpoint...")
        async with session.get(f"{base_url}/user/elonmusk/tweets?limit=3") as response:
            data = await response.json()
            print(f"   ✅ Found {data.get('count', 0)} tweets from user")
        
        # Test 5: Trending
        print("\n5️⃣ Testing trending endpoint...")
        async with session.get(f"{base_url}/trending") as response:
            data = await response.json()
            print(f"   ✅ Found {data.get('count', 0)} trending topics")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    print("Make sure the API is running on http://localhost:8000")
    print("Start it with: python main.py\n")
    
    try:
        asyncio.run(test_api())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the API is running!")

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import SearchResult, Base

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama Server URL
OLLAMA_SERVER_URL = "http://144.24.149.254:11435/api/generate"

# Google Custom Search API Configuration
GOOGLE_API_KEY = "AIzaSyBowr2JsRDrr1G5P6QE85MJ3_SWCkREw_M"
GOOGLE_CX = "10c5cac10681841f7"
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# YouTube API Configuration
YOUTUBE_API_KEY = "AIzaSyB8y0g6ZK9UHDsH88Mkmguf_3L1nLVUTZE"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# Request model (takes only 'query' from the user)
class QueryRequest(BaseModel):
    query: str  

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def generate_relevant_queries(query: str):
    """Generates alternate queries using Ollama AI."""
    prompt = f"Generate 5 alternate feasible relevant queries similar to: '{query}' which are helpful to search in Google and YouTube."
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(OLLAMA_SERVER_URL, json={
                "model": "gemma:2b",  
                "prompt": prompt,
                "stream": False
            }) as response:
                response.raise_for_status()
                data = await response.json()
                ai_response = data.get("response", "").strip()
                if not ai_response:
                    return ["No relevant queries generated."]
                
                alternative_queries = ai_response.split("\n")
                return alternative_queries[:3]  # Return only the first 3 queries
        
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to get response from Ollama: {str(e)}")

async def search_google(query: str):
    """Searches Google using the 1st alternate query."""
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(GOOGLE_SEARCH_URL, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("items", [])[:5]  # Return top 5 search results
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to get Google Search results: {str(e)}")

async def search_youtube(query: str):
    """Searches YouTube using the 2nd alternate query."""
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 6,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(YOUTUBE_SEARCH_URL, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                videos = [
                    {
                        "title": item["snippet"]["title"],
                        "videoId": item["id"]["videoId"],
                        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                        "channel": item["snippet"]["channelTitle"],
                        "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                    }
                    for item in data.get("items", [])
                ]
                return videos
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to get YouTube search results: {str(e)}")

def rank_results(results, query):
    """Ranks search results based on relevance and popularity."""
    for result in results:
        relevance_score = result.snippet.lower().count(query.lower()) * 2  # Count keyword matches
        popularity_score = result.rank_score  # Example: You can set this based on views
        result.rank_score = relevance_score + popularity_score

    return sorted(results, key=lambda x: x.rank_score, reverse=True)

@app.post("/ask-ai/")
async def ask_ai(request: QueryRequest, db: Session = Depends(get_db)):
    """Generates alternative queries, fetches Google & YouTube search results, and stores ranked data."""
    alternative_queries = await generate_relevant_queries(request.query)
    
    google_results = []
    youtube_results = []
    
    if len(alternative_queries) >= 2 and alternative_queries[0] != "No relevant queries generated.":
        google_results = await search_google(alternative_queries[0])  # 1st query for Google
        youtube_results = await search_youtube(alternative_queries[1])  # 2nd query for YouTube

        # Store results in MySQL with ranking
        all_results = []
        for result in google_results:
            all_results.append(SearchResult(
                query=request.query,
                source="Google",
                title=result["title"],
                link=result["link"],
                snippet=result.get("snippet", ""),
                rank_score=0.0  # Will be updated after ranking
            ))

        for result in youtube_results:
            all_results.append(SearchResult(
                query=request.query,
                source="YouTube",
                title=result["title"],
                link=result["link"],
                snippet=result["channel"],
                rank_score=0.0  # Will be updated after ranking
            ))

        # Apply ranking
        ranked_results = rank_results(all_results, request.query)

        # Store in MySQL
        db.bulk_save_objects(ranked_results)
        db.commit()

        print("✅ Results stored successfully!")

    return {
        "query": request.query,
        "alternative_queries": alternative_queries,
        "google_results": google_results,
        "youtube_results": youtube_results
    }

@app.get("/get_results/")
async def get_results(query: str, db: Session = Depends(get_db)):
    """Fetches ranked results from MySQL."""
    results = db.query(SearchResult).filter(SearchResult.query == query).order_by(SearchResult.rank_score.desc()).all()
    return results

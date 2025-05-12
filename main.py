from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from openai import OpenAI
from news_api import fetch_news
from summarizer import extract_tips

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")

# Validate API keys
if not OPENAI_API_KEY:
    raise HTTPException(status_code=500, detail="OPENAI_API_KEY not found in environment variables")
if not NEWSAPI_API_KEY:
    raise HTTPException(status_code=500, detail="NEWSAPI_API_KEY not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# Define the endpoint
@app.get("/summarize-disaster-news")
async def get_tips_from_disaster_news(disaster: str, user_role: str):
    # Fetch news articles
    articles = fetch_news(disaster, NEWSAPI_API_KEY)

    # Summarize articles
    summaries = extract_tips(articles, user_role, client)

    # Check if any summaries were generated
    if not summaries:
        raise HTTPException(status_code=500, detail="Failed to generate any summaries")

    # Return results
    return {"disaster": disaster, "summaries": summaries}

# Run the app (for development)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

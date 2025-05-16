from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import os
from openai import OpenAI
from summarizer import get_tips
from suggester import get_suggestion

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API keys
if not OPENAI_API_KEY:
    raise HTTPException(status_code=500, detail="OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# Define the endpoint
@app.get("/summarize-disaster-news")
async def get_tips_from_disaster_news(
        disaster: str = Query(..., min_length=1, description="Disaster name and location"),
        user_role: str = Query(..., min_length=1, description="User role")
):
    if not disaster.strip():
        raise HTTPException(status_code=422, detail="Disaster parameter cannot be empty or whitespace")

    try:
        # Generate summary using ChatGPT
        summary = get_tips(disaster, user_role, client)

        # Check if summary is generated
        if not summary.strip():
            raise HTTPException(status_code=500, detail="Failed to generate a valid summary")

        # Return results
        return {"disaster": disaster, "summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/suggest-need-level")
async def suggest_need_level(
        request_text: str = Query(..., min_length=1, description="Text to be suggested")
):
    if not request_text.strip():
        raise HTTPException(status_code=422, detail="Text to be suggested")

    try:
        answer = get_suggestion(request_text, client)

        if not answer.strip():
            raise HTTPException(status_code=500, detail="Failed to generate a valid suggestion")

        return {"suggestedNeedLevel": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# Run the app (for development)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

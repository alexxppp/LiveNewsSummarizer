import requests
from fastapi import HTTPException


def fetch_news(keyword: str, api_key: str) -> list[dict[str, str]]:
    """
    Fetch news articles about a specific disaster from NewsAPI.

    Args:
        keyword: The disaster's name, location, etc...
        api_key: NewsAPI key.

    Returns:
        List of dictionaries with title and description for each article.

    Raises:
        HTTPException: If the API call fails or no articles are found.
    """
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}&language=en&sortBy=publishedAt&pageSize=5"
    response = requests.get(url)

    # Check for HTTP errors
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch news from NewsAPI")

    data = response.json()
    if data.get("status") != "ok":
        raise HTTPException(status_code=500, detail="NewsAPI error")

    articles = data.get("articles", [])
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the specified disaster")

    # Extract title and description
    return [{"title": article.get("title", ""), "description": article.get("description", "")} for article in articles]

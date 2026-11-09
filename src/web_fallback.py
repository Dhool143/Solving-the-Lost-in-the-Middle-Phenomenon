
import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def search_web(query: str, max_results: int = 3) -> list[dict]:
    """Search the web when internal retrieval confidence is low."""

    if not query.strip():
        return []

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is missing. Add it to your .env file."
        )

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        max_results=max_results,
        search_depth="basic",
    )

    chunks = []

    for index, result in enumerate(response.get("results", [])):
        url = result.get("url", "")
        content = result.get("content", "")

        if not url or not content:
            continue

        chunks.append({
            "chunk_id": f"web-{index + 1}",
            "content": content,
            "score": float(result.get("score", 0.0)),
            "source": "web",
            "url": url,
        })

    return chunks

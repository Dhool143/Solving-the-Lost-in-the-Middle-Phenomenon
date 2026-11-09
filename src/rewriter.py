
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def rewrite_query(query: str, history: str = "") -> str:
    """Rewrite a user's question into a clear search query."""

    if not query.strip():
        return ""

    api_key = os.getenv("OPENAI_API_KEY")

    # Return the original question if no API key is available.
    if not api_key:
        return query.strip()

    client = OpenAI(api_key=api_key, timeout=10.0)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Rewrite the user's latest question as a clear, "
                        "standalone search query. Use conversation history "
                        "to resolve pronouns. Preserve exact technical "
                        "names, IDs, commands, and version numbers. "
                        "Do not answer the question."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Conversation history:\n{history}\n\n"
                        f"Latest question:\n{query}"
                    ),
                },
            ],
            temperature=0,
        )

        rewritten = response.choices[0].message.content
        return rewritten.strip() if rewritten else query.strip()

    except Exception:
        return query.strip()

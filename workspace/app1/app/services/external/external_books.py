# /services/external/external_books.py
#
# - Uses httpx/tenacity.
# - Provides a function to fetch book data from the ***EXTERNAL*** Open Library API 
# - Implements retry logic with tenacity to handle transient errors.
# 


from typing import Any
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

BASE_URL = "https://openlibrary.org/search.json"




@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True,
)
async def fetch_one_book(query: str) -> dict[str, Any] | None:
    params = {"q": query, "limit": 1}
    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    docs = data.get("docs", [])
    if not docs:
        return None

    doc = docs[0]
    return {
        "title": doc.get("title"),
        "first_publish_year": doc.get("first_publish_year"),
        "author": ", ".join(doc.get("author_name", [])) if doc.get("author_name") else None,
        "isbn": doc.get("isbn", [None])[0] if doc.get("isbn") else None,
    }

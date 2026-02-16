# /routers/import_books.py
#
# - Defines a POST endpoint to import book data from Open Library API based on a query string.
# - Uses the service layer to fetch book data and upsert it into the database.
# - Handles errors for not found and database issues, returning appropriate HTTP status codes.
#


from fastapi import APIRouter, HTTPException
from app.services.external.external_books import fetch_one_book
from app.services.db.items_sql import upsert_item_from_book

# router = APIRouter(prefix="/api", tags=["import"])
router = APIRouter(tags=["import"])


@router.post("/import/book")
async def import_book(q: str):
    book = await fetch_one_book(q)
    if not book:
        raise HTTPException(status_code=404, detail="No book found")

    try:
        row = upsert_item_from_book(book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB insert failed: {e}")

    return {
        "external": book,
        "stored_item": row,
    }

# /services/db/items_sql.py
#
# I is a service module for database operations related to "items".
# It actually, stores in the db the book data fetched from the external API, but it is not aware of the external API at all.
# This module provides a function to upsert an item into the `items` table based on book data.
# - Uses pure SQL with PyMySQL connection.


from typing import Any
from app.core.database import get_conn


def upsert_item_from_book(book: dict[str, Any]) -> dict[str, Any]:
    """
    Inserts a book into `items` using pure SQL.
    - itemName <- book['title']
    - itemModelYear <- book['first_publish_year']
    - itemListPrice <- 0.00 (placeholder)
    Returns the inserted or existing row.
    """

    title = (book.get("title") or "").strip()
    if not title:
        raise ValueError("Book title missing")

    model_year = book.get("first_publish_year")
    price = 0.00  # your schema requires a price; external API doesn't provide it

    with get_conn() as conn:
        with conn.cursor() as cur:
            # 1) check if already exists by name (simple dedupe strategy)
            cur.execute(
                "SELECT itemId, itemName, itemListPrice, itemModelYear "
                "FROM items WHERE itemName = %s LIMIT 1",
                (title,),
            )
            existing = cur.fetchone()
            if existing:
                return existing

            # 2) insert
            cur.execute(
                "INSERT INTO items (itemName, itemListPrice, itemModelYear, itemStatusId) "
                "VALUES (%s, %s, %s, 1)",
                (title, price, model_year),
            )

            item_id = cur.lastrowid
            print(f"[***** items_sql] inserted itemId={item_id} title={title!r}")

            # 3) return inserted row
            cur.execute(
                "SELECT itemId, itemName, itemListPrice, itemModelYear "
                "FROM items WHERE itemId = %s",
                (item_id,),
            )
            return cur.fetchone()

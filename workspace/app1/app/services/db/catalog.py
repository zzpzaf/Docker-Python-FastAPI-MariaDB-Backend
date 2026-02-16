# app/services/catalog.py
# Using pure SQL queries 
#
# Contains pure SQL queries
# Each method:
#   opens a cursor using a conn object passed from the router (no connection pooling or management here)
#   executes SQL with safe parameter binding (%s)
#   returns dict rows (DictCursor)
#
# 260215: Added write methods (POST-PUT-PATCH-DELETE) for both Categories and Items, with proper error handling and transaction management.

from typing import Any
import pymysql
from pymysql.err import IntegrityError



class CatalogService:
    # -------------------------
    # READ Categories (GET) 
    # -------------------------
    @staticmethod
    def list_categories(conn: pymysql.Connection) -> list[dict[str, Any]]:
        sql = """
            SELECT
              categoryId,
              categoryName,
              categoryStatusId,
              categoryCrUUID,
              categoryCrTimestamp,
              categoryClientUUID
            FROM categories
            ORDER BY categoryName
        """
        with conn.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())

    @staticmethod
    def get_category(conn: pymysql.Connection, category_id: int) -> dict[str, Any] | None:
        sql = """
            SELECT
              categoryId,
              categoryName,
              categoryStatusId,
              categoryCrUUID,
              categoryCrTimestamp,
              categoryClientUUID
            FROM categories
            WHERE categoryId = %s
        """
        with conn.cursor() as cur:
            cur.execute(sql, (category_id,))
            return cur.fetchone()

    # -------------------------
    # READ Items (GET) 
    # -------------------------
    @staticmethod
    def list_items(conn: pymysql.Connection) -> list[dict[str, Any]]:
        sql = """
            SELECT
              itemId,
              itemName,
              itemListPrice,
              itemModelYear,
              itemStatusId,
              itemCrUUID,
              itemCrTimestamp,
              itemClientUUID
            FROM items
            ORDER BY itemName
        """
        with conn.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())

    @staticmethod
    def get_item(conn: pymysql.Connection, item_id: int) -> dict[str, Any] | None:
        sql = """
            SELECT
              itemId,
              itemName,
              itemListPrice,
              itemModelYear,
              itemStatusId,
              itemCrUUID,
              itemCrTimestamp,
              itemClientUUID
            FROM items
            WHERE itemId = %s
        """
        with conn.cursor() as cur:
            cur.execute(sql, (item_id,))
            return cur.fetchone()


    # -----------------------------------------
    # READ category-items Relations (GET)  
    # -----------------------------------------
    @staticmethod
    def list_items_for_category(conn: pymysql.Connection, category_id: int) -> list[dict[str, Any]] | None:
        # Verify category exists
        if not CatalogService.get_category(conn, category_id):
            return None

        sql = """
            SELECT
              i.itemId,
              i.itemName,
              i.itemListPrice,
              i.itemModelYear,
              i.itemStatusId,
              i.itemCrUUID,
              i.itemCrTimestamp,
              i.itemClientUUID
            FROM items i
            JOIN categoryitems ci
              ON ci.categoryitemItemId = i.itemId
            WHERE ci.categoryitemCategoryId = %s
            ORDER BY i.itemName
        """
        with conn.cursor() as cur:
            cur.execute(sql, (category_id,))
            return list(cur.fetchall())

    @staticmethod
    def list_categories_for_item(conn: pymysql.Connection, item_id: int) -> list[dict[str, Any]] | None:
        # Verify item exists
        if not CatalogService.get_item(conn, item_id):
            return None

        sql = """
            SELECT
              c.categoryId,
              c.categoryName,
              c.categoryStatusId,
              c.categoryCrUUID,
              c.categoryCrTimestamp,
              c.categoryClientUUID
            FROM categories c
            JOIN categoryitems ci
              ON ci.categoryitemCategoryId = c.categoryId
            WHERE ci.categoryitemItemId = %s
            ORDER BY c.categoryName
        """
        with conn.cursor() as cur:
            cur.execute(sql, (item_id,))
            return list(cur.fetchall())
        


    # ------------------------------------------
    # WRITE Categories (POST-PUT-PATCH-DELETE) 
    # ------------------------------------------
    @staticmethod
    def create_category(conn: pymysql.Connection, data: dict[str, Any]) -> dict[str, Any]:
        sql = """
            INSERT INTO categories (categoryName, categoryStatusId, categoryClientUUID)
            VALUES (%s, %s, %s)
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (data["categoryName"], data["categoryStatusId"], data.get("categoryClientUUID")))
                new_id = cur.lastrowid
            conn.commit()
            return CatalogService.get_category(conn, int(new_id))  # type: ignore[arg-type]
        except IntegrityError:
            conn.rollback()
            raise

    @staticmethod
    def put_category(conn: pymysql.Connection, category_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        if not CatalogService.get_category(conn, category_id):
            return None

        sql = """
            UPDATE categories
            SET categoryName=%s,
                categoryStatusId=%s,
                categoryClientUUID=%s
            WHERE categoryId=%s
        """
        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        data["categoryName"],
                        data["categoryStatusId"],
                        data.get("categoryClientUUID"),
                        category_id,
                    ),
                )
            conn.commit()
            return CatalogService.get_category(conn, category_id)
        except IntegrityError:
            conn.rollback()
            raise

    @staticmethod
    def patch_category(conn: pymysql.Connection, category_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        existing = CatalogService.get_category(conn, category_id)
        if not existing:
            return None

        fields = []
        params: list[Any] = []

        for col in ("categoryName", "categoryStatusId", "categoryClientUUID"):
            if col in data and data[col] is not None:
                fields.append(f"{col}=%s")
                params.append(data[col])

        if not fields:
            # Nothing to update; return existing record
            return existing

        sql = f"UPDATE categories SET {', '.join(fields)} WHERE categoryId=%s"
        params.append(category_id)

        try:
            with conn.cursor() as cur:
                cur.execute(sql, tuple(params))
            conn.commit()
            return CatalogService.get_category(conn, category_id)
        except IntegrityError:
            conn.rollback()
            raise

    @staticmethod
    def delete_category(conn: pymysql.Connection, category_id: int) -> bool:
        sql = "DELETE FROM categories WHERE categoryId=%s"
        with conn.cursor() as cur:
            cur.execute(sql, (category_id,))
            affected = cur.rowcount
        conn.commit()
        return affected > 0


    # --------------------------------------
    # WRITE Items (POST-PUT-PATCH-DELETE) 
    # --------------------------------------
    @staticmethod
    def create_item(conn: pymysql.Connection, data: dict[str, Any]) -> dict[str, Any]:
        sql = """
            INSERT INTO items (itemName, itemListPrice, itemModelYear, itemStatusId, itemClientUUID)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        data["itemName"],
                        data["itemListPrice"],
                        data.get("itemModelYear"),
                        data["itemStatusId"],
                        data.get("itemClientUUID"),
                    ),
                )
                new_id = cur.lastrowid
            conn.commit()
            return CatalogService.get_item(conn, int(new_id))  # type: ignore[arg-type]
        except IntegrityError:
            conn.rollback()
            raise

    @staticmethod
    def put_item(conn: pymysql.Connection, item_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        if not CatalogService.get_item(conn, item_id):
            return None

        sql = """
            UPDATE items
            SET itemName=%s,
                itemListPrice=%s,
                itemModelYear=%s,
                itemStatusId=%s,
                itemClientUUID=%s
            WHERE itemId=%s
        """
        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        data["itemName"],
                        data["itemListPrice"],
                        data.get("itemModelYear"),
                        data["itemStatusId"],
                        data.get("itemClientUUID"),
                        item_id,
                    ),
                )
            conn.commit()
            return CatalogService.get_item(conn, item_id)
        except IntegrityError:
            conn.rollback()
            raise

    @staticmethod
    def patch_item(conn: pymysql.Connection, item_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        existing = CatalogService.get_item(conn, item_id)
        if not existing:
            return None

        fields = []
        params: list[Any] = []

        for col in ("itemName", "itemListPrice", "itemModelYear", "itemStatusId", "itemClientUUID"):
            if col in data and data[col] is not None:
                fields.append(f"{col}=%s")
                params.append(data[col])

        if not fields:
            return existing

        sql = f"UPDATE items SET {', '.join(fields)} WHERE itemId=%s"
        params.append(item_id)

        try:
            with conn.cursor() as cur:
                cur.execute(sql, tuple(params))
            conn.commit()
            return CatalogService.get_item(conn, item_id)
        except IntegrityError:
            conn.rollback()
            raise

    @staticmethod
    def delete_item(conn: pymysql.Connection, item_id: int) -> bool:
        sql = "DELETE FROM items WHERE itemId=%s"
        with conn.cursor() as cur:
            cur.execute(sql, (item_id,))
            affected = cur.rowcount
        conn.commit()
        return affected > 0

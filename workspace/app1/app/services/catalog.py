# app/services/catalog.py
# Using pure SQL queries 
#
# Contains pure SQL queries
# Each method:
#   opens a cursor
#   executes SQL with safe parameter binding (%s)
#   returns dict rows (DictCursor)

from typing import Any
import pymysql


class CatalogService:
    # -------------------------
    # Categories
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
    # Items
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

    # -------------------------
    # Relations
    # -------------------------
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

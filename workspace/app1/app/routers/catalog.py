# app/routers/catalog.py
# (GET endpoints; returns dicts)
#
# Defines endpoints
# Calls service layer
# Converts missing rows to HTTP 404

from fastapi import APIRouter, Depends, HTTPException
import pymysql

from app.core.database import get_db
from app.schemas import (
    CategoryRead,
    ItemRead,
    CategoryReadWithItems,
    ItemReadWithCategories,
)
from app.services.catalog import CatalogService

router = APIRouter(tags=["catalog"])


@router.get("/categories", response_model=list[CategoryRead])
def get_categories(conn: pymysql.Connection = Depends(get_db)):
    return CatalogService.list_categories(conn)


@router.get("/categories/{category_id}", response_model=CategoryReadWithItems)
def get_category(category_id: int, conn: pymysql.Connection = Depends(get_db)):
    cat = CatalogService.get_category(conn, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    cat["items"] = CatalogService.list_items_for_category(conn, category_id) or []
    return cat


@router.get("/items", response_model=list[ItemRead])
def get_items(conn: pymysql.Connection = Depends(get_db)):
    return CatalogService.list_items(conn)


@router.get("/items/{item_id}", response_model=ItemReadWithCategories)
def get_item(item_id: int, conn: pymysql.Connection = Depends(get_db)):
    item = CatalogService.get_item(conn, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item["categories"] = CatalogService.list_categories_for_item(conn, item_id) or []
    return item


@router.get("/categories/{category_id}/items", response_model=list[ItemRead])
def get_items_for_category(category_id: int, conn: pymysql.Connection = Depends(get_db)):
    items = CatalogService.list_items_for_category(conn, category_id)
    if items is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return items


@router.get("/items/{item_id}/categories", response_model=list[CategoryRead])
def get_categories_for_item(item_id: int, conn: pymysql.Connection = Depends(get_db)):
    cats = CatalogService.list_categories_for_item(conn, item_id)
    if cats is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return cats

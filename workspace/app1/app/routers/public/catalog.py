# app/routers/catalog.py
# (GET endpoints; returns dicts)
#
# Defines endpoints
# Calls service layer
# Converts missing rows to HTTP 404
#
# 260215: Added write endpoints (POST-PUT-PATCH-DELETE) for both Categories and Items, with proper error handling for 404 and 409 cases.



from fastapi import APIRouter, Depends, HTTPException, status
import pymysql
from pymysql.err import IntegrityError


from app.core.database import get_db
from app.schemas import (
    CategoryRead,
    CategoryReadWithItems,
    CategoryCreate,
    CategoryPut,
    CategoryPatch,
    ItemRead,
    ItemReadWithCategories,
    ItemCreate,
    ItemPut,
    ItemPatch,
)
from app.services.db.catalog import CatalogService

router = APIRouter(tags=["catalog"])


# -------------------------
# READ Categories (GET)
# -------------------------

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


# ------------------------------------------
# WRITE Categories (POST-PUT-PATCH-DELETE)
# ------------------------------------------
@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, conn: pymysql.Connection = Depends(get_db)):
    try:
        return CatalogService.create_category(conn, payload.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Category name already exists")


@router.put("/categories/{category_id}", response_model=CategoryRead)
def put_category(category_id: int, payload: CategoryPut, conn: pymysql.Connection = Depends(get_db)):
    try:
        updated = CatalogService.put_category(conn, category_id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Category not found")
        return updated
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Category name already exists")


@router.patch("/categories/{category_id}", response_model=CategoryRead)
def patch_category(category_id: int, payload: CategoryPatch, conn: pymysql.Connection = Depends(get_db)):
    # only send fields that user actually provided
    # without exclude_unset=True, optional fields not provided by the client may appear as None and accidentally overwrite DB values.
    data = payload.model_dump(exclude_unset=True)
    try:
        updated = CatalogService.patch_category(conn, category_id, data)
        if not updated:
            raise HTTPException(status_code=404, detail="Category not found")
        return updated
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Category name already exists")


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, conn: pymysql.Connection = Depends(get_db)):
    deleted = CatalogService.delete_category(conn, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return None







# -------------------------
# READ Items (GET)
# -------------------------

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


# --------------------------------------
# WRITE Items (POST-PUT-PATCH-DELETE)
# --------------------------------------

@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, conn: pymysql.Connection = Depends(get_db)):
    try:
        return CatalogService.create_item(conn, payload.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Item already exists or violates constraints")


@router.put("/items/{item_id}", response_model=ItemRead)
def put_item(item_id: int, payload: ItemPut, conn: pymysql.Connection = Depends(get_db)):
    try:
        updated = CatalogService.put_item(conn, item_id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Item not found")
        return updated
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Update violates constraints")


@router.patch("/items/{item_id}", response_model=ItemRead)
def patch_item(item_id: int, payload: ItemPatch, conn: pymysql.Connection = Depends(get_db)):
    # without exclude_unset=True, optional fields not provided by the client may appear as None and accidentally overwrite DB values.
    data = payload.model_dump(exclude_unset=True)
    try:
        updated = CatalogService.patch_item(conn, item_id, data)
        if not updated:
            raise HTTPException(status_code=404, detail="Item not found")
        return updated
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Update violates constraints")


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, conn: pymysql.Connection = Depends(get_db)):
    deleted = CatalogService.delete_item(conn, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return None





# -----------------------------------------
# READ category-items Relations (GET)
# -----------------------------------------


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

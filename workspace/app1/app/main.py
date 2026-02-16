# workspace/app1/app/main.py 
# 
# Creates FastAPI app
# Includes routers for health + catalog endpoints



from fastapi import FastAPI
from app.core.config import settings
from app.routers.public import health_router, catalog_router, import_books_router


app = FastAPI(title=settings.app_name)

app.include_router(health_router) # just /health, no prefix
app.include_router(health_router, prefix=settings.api_prefix)  # /api/health


# app.include_router(catalog_router)
app.include_router(catalog_router, prefix=settings.api_prefix)

# 260216: Added import_books_router for POST /api/import/book endpoint to fetch book data from Open Library and store it in the database.
app.include_router(import_books_router, prefix=settings.api_prefix)

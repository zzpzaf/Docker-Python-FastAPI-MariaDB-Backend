# app/routers/__init__.py
from .health import router as health_router
from .catalog import router as catalog_router

__all__ = ["health_router", "catalog_router"]


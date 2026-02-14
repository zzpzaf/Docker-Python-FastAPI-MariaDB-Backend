# app/schemas/category.py 
# (Pydantic v2)
#
# Defines output shapes for API responses
# Validates and filters returned dicts (extra fields ignored)



from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class CategoryRead(BaseModel):
    """
    Mirrors the `categories` table (read-only for now).
    """
    model_config = ConfigDict(extra="ignore")

    categoryId: int = Field(..., ge=1)
    categoryName: str
    categoryStatusId: int = Field(..., ge=0, le=65535)  # SMALLINT UNSIGNED
    categoryCrUUID: str  # CHAR(36)
    categoryCrTimestamp: datetime
    categoryClientUUID: str | None = None


class CategoryReadWithItems(CategoryRead):
    items: list["ItemRead"] = []


from .item import ItemRead  # noqa: E402
CategoryReadWithItems.model_rebuild()

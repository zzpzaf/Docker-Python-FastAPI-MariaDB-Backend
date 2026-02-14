# app/schemas/item.py 
# (Pydantic v2)
#
# Defines output shapes for API responses
# Validates and filters returned dicts (extra fields ignored)



from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ItemRead(BaseModel):
    """
    Mirrors the `items` table (read-only for now).
    """
    model_config = ConfigDict(extra="ignore")

    itemId: int = Field(..., ge=1)
    itemName: str
    itemListPrice: Decimal  # DECIMAL(10,2)
    itemModelYear: int | None = Field(default=None, ge=0, le=65535)  # SMALLINT UNSIGNED NULL
    itemStatusId: int = Field(..., ge=0, le=65535)  # SMALLINT UNSIGNED
    itemCrUUID: str  # CHAR(36)
    itemCrTimestamp: datetime
    itemClientUUID: str | None = None


class ItemReadWithCategories(ItemRead):
    categories: list["CategoryRead"] = []


from .category import CategoryRead  # noqa: E402
ItemReadWithCategories.model_rebuild()


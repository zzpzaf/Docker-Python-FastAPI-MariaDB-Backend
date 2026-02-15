# app/schemas/item.py 
# (Pydantic v2)
#
# Defines output shapes (Pydantic models/classes) for API responses
# Validates and filters returned dicts (extra fields ignored)
#
# 260215: Classes Added:  
#    - ItemCreate: for POST endpoints; all fields except auto-generated ones are required (client sends full state of mutable fields)
#    - ItemPut: for PUT endpoints; all fields are required (client sends full state of mutable fields)
#    - ItemPatch: for PATCH endpoints


from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ItemRead(BaseModel):

    # extra fields ignored (e.g. from DB rows with more columns, or from joins)
    model_config = ConfigDict(extra="ignore")

    itemId: int = Field(..., ge=1)
    itemName: str
    itemListPrice: Decimal  # DECIMAL(10,2)
    itemModelYear: int | None = Field(default=None, ge=0, le=65535)  # SMALLINT UNSIGNED NULL
    itemStatusId: int = Field(..., ge=0, le=65535)  # SMALLINT UNSIGNED
    itemCrUUID: str  # CHAR(36)
    itemCrTimestamp: datetime
    itemClientUUID: str | None = None

# POST is for creating new resources, so all fields except auto-generated ones are required (client sends full state of mutable fields)
class ItemCreate(BaseModel):
    itemName: str = Field(..., min_length=1, max_length=100)
    itemListPrice: Decimal
    itemModelYear: int | None = Field(default=None, ge=0, le=65535)
    itemStatusId: int = Field(default=1, ge=0, le=65535)
    itemClientUUID: str | None = Field(default=None, max_length=40)

# PUT is for full updates, so all fields are required (client sends full state of mutable fields)
class ItemPut(BaseModel):
    itemName: str = Field(..., min_length=1, max_length=100)
    itemListPrice: Decimal
    itemModelYear: int | None = Field(default=None, ge=0, le=65535)
    itemStatusId: int = Field(default=1, ge=0, le=65535)
    itemClientUUID: str | None = Field(default=None, max_length=40)

# PATCH is for partial updates, so all fields are optional (client sends only changed fields)
class ItemPatch(BaseModel):
    itemName: str | None = Field(default=None, min_length=1, max_length=100)
    itemListPrice: Decimal | None = None
    itemModelYear: int | None = Field(default=None, ge=0, le=65535)
    itemStatusId: int | None = Field(default=None, ge=0, le=65535)
    itemClientUUID: str | None = Field(default=None, max_length=40)







class ItemReadWithCategories(ItemRead):
    categories: list["CategoryRead"] = []


from .category import CategoryRead  # noqa: E402
ItemReadWithCategories.model_rebuild()


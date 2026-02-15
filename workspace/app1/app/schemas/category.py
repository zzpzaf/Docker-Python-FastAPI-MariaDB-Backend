# app/schemas/category.py 
# (Pydantic v2)
#
# Defines output shapes (Pydantic models/classes) for API responses
# Validates and filters returned dicts (extra fields ignored)

# 260215: Classes Added:  
#    - CategoryCreate: for POST endpoints; all fields except auto-generated ones are required (client sends full state of mutable fields)
#    - CategoryPut: for PUT endpoints; all fields are required (client sends full state of mutable fields)
#    - CategoryPatch: for PATCH endpoints



from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# Mirrors the `categories` table structure, but with Pydantic validation.

# READ (GET) is for returning data to clients, so all fields are required (except clientUUID which is optional), but extra fields are ignored (e.g. from DB rows with more columns, or from joins) 
class CategoryRead(BaseModel):

    # extra fields ignored (e.g. from DB rows with more columns, or from joins)
    model_config = ConfigDict(extra="ignore")

    categoryId: int = Field(..., ge=1)
    categoryName: str
    categoryStatusId: int = Field(..., ge=0, le=65535)  # SMALLINT UNSIGNED
    categoryCrUUID: str  # CHAR(36)
    categoryCrTimestamp: datetime
    categoryClientUUID: str | None = None


# POST is for creating new resources, so all fields except auto-generated ones are required (client sends full state of mutable fields)
class CategoryCreate(BaseModel):
    categoryName: str = Field(..., min_length=1, max_length=100)
    categoryStatusId: int = Field(default=1, ge=0, le=65535)
    categoryClientUUID: str | None = Field(default=None, max_length=40)

# PUT is for full updates, so all fields are required (client sends full state of mutable fields)
class CategoryPut(BaseModel):
    # full update (client sends full state of mutable fields)
    categoryName: str = Field(..., min_length=1, max_length=100)
    categoryStatusId: int = Field(default=1, ge=0, le=65535)
    categoryClientUUID: str | None = Field(default=None, max_length=40)

# PATCH is for partial updates, so all fields are optional (client sends only changed fields)
class CategoryPatch(BaseModel):
    # partial update (all optional)
    categoryName: str | None = Field(default=None, min_length=1, max_length=100)
    categoryStatusId: int | None = Field(default=None, ge=0, le=65535)
    categoryClientUUID: str | None = Field(default=None, max_length=40)




class CategoryReadWithItems(CategoryRead):
    items: list["ItemRead"] = []


from .item import ItemRead  # noqa: E402
CategoryReadWithItems.model_rebuild()

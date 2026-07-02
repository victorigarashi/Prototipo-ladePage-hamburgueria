from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ComboCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=160)
    description: str = Field(..., min_length=5)
    items: list[str] = Field(default_factory=list)
    price: Decimal = Field(..., gt=0)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = True
    is_available: bool = True


class ComboUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, min_length=5)
    items: list[str] | None = None
    price: Decimal | None = Field(default=None, gt=0)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None
    is_available: bool | None = None


class ComboResponse(BaseModel):
    id: int
    name: str
    description: str
    items: list[str]
    price: Decimal
    image_url: str | None
    is_active: bool
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

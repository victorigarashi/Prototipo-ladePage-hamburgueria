from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.schemas.category_schema import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=160)
    description: str = Field(..., min_length=5)
    price: Decimal = Field(..., gt=0)
    category_id: int
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = True
    is_available: bool = True

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, min_length=5)
    price: Decimal | None = Field(default=None, gt=0)
    category_id: int | None = None
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None
    is_available: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    category_id: int
    image_url: str | None
    is_active: bool
    is_available: bool
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse

    model_config = {"from_attributes": True}

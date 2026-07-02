from datetime import datetime

from pydantic import BaseModel, Field


class PromotionCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=160)
    description: str = Field(..., min_length=5)
    code: str | None = Field(default=None, max_length=80)
    discount: str | None = Field(default=None, max_length=120)
    is_active: bool = True


class PromotionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, min_length=5)
    code: str | None = Field(default=None, max_length=80)
    discount: str | None = Field(default=None, max_length=120)
    is_active: bool | None = None


class PromotionResponse(BaseModel):
    id: int
    title: str
    description: str
    code: str | None
    discount: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category_schema import CategoryResponse
from app.services.category_service import list_categories


router = APIRouter(prefix="/categories", tags=["Categorias públicas"])


@router.get("", response_model=list[CategoryResponse])
def public_categories(db: Session = Depends(get_db)):
    return list_categories(db, only_active=True)

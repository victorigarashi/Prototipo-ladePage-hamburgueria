import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "categoria"


def list_categories(db: Session, only_active: bool = False) -> list[Category]:
    query = db.query(Category).order_by(Category.name.asc())
    if only_active:
        query = query.filter(Category.is_active.is_(True))
    return query.all()


def get_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    slug = payload.slug or slugify(payload.name)
    if db.query(Category).filter(Category.slug == slug).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug de categoria já existe.")

    category = Category(name=payload.name, slug=slug, is_active=payload.is_active)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, payload: CategoryUpdate) -> Category:
    category = get_category(db, category_id)
    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        category.name = data["name"]
    if "slug" in data:
        category.slug = data["slug"] or slugify(category.name)
    if "is_active" in data:
        category.is_active = data["is_active"]
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    if category.products:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Categoria possui produtos vinculados.")
    db.delete(category)
    db.commit()

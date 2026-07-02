import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.combo_model import Combo
from app.schemas.combo_schema import ComboCreate, ComboUpdate


def serialize_items(items: list[str]) -> str:
    return json.dumps(items, ensure_ascii=False)


def parse_combo(combo: Combo) -> Combo:
    combo.items = json.loads(combo.items or "[]")
    return combo


def list_public_combos(db: Session) -> list[Combo]:
    return [parse_combo(combo) for combo in db.query(Combo).filter(Combo.is_active.is_(True)).order_by(Combo.created_at.desc()).all()]


def list_admin_combos(db: Session) -> list[Combo]:
    return [parse_combo(combo) for combo in db.query(Combo).order_by(Combo.created_at.desc()).all()]


def get_combo(db: Session, combo_id: int) -> Combo:
    combo = db.get(Combo, combo_id)
    if not combo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Combo não encontrado.")
    return parse_combo(combo)


def create_combo(db: Session, payload: ComboCreate) -> Combo:
    data = payload.model_dump()
    data["items"] = serialize_items(data["items"])
    combo = Combo(**data)
    db.add(combo)
    db.commit()
    db.refresh(combo)
    return get_combo(db, combo.id)


def update_combo(db: Session, combo_id: int, payload: ComboUpdate) -> Combo:
    combo = db.get(Combo, combo_id)
    if not combo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Combo não encontrado.")
    data = payload.model_dump(exclude_unset=True)
    if "items" in data:
        data["items"] = serialize_items(data["items"])
    for field, value in data.items():
        setattr(combo, field, value)
    db.commit()
    db.refresh(combo)
    return get_combo(db, combo.id)


def delete_combo(db: Session, combo_id: int) -> None:
    combo = db.get(Combo, combo_id)
    if not combo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Combo não encontrado.")
    db.delete(combo)
    db.commit()


def toggle_combo_active(db: Session, combo_id: int) -> Combo:
    combo = db.get(Combo, combo_id)
    if not combo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Combo não encontrado.")
    combo.is_active = not combo.is_active
    db.commit()
    db.refresh(combo)
    return get_combo(db, combo.id)


def toggle_combo_available(db: Session, combo_id: int) -> Combo:
    combo = db.get(Combo, combo_id)
    if not combo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Combo não encontrado.")
    combo.is_available = not combo.is_available
    db.commit()
    db.refresh(combo)
    return get_combo(db, combo.id)

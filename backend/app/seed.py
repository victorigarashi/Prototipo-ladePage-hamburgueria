from decimal import Decimal

from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models.category_model import Category
from app.models.combo_model import Combo
from app.models.product_model import Product
from app.models.promotion_model import Promotion
from app.models.user_model import User
from app.security import hash_password


def upsert_category(db: Session, name: str, slug: str) -> Category:
    category = db.query(Category).filter(Category.slug == slug).first()
    if category:
        category.name = name
        category.is_active = True
        return category

    category = Category(name=name, slug=slug, is_active=True)
    db.add(category)
    db.flush()
    return category


def upsert_product(db: Session, **data) -> Product:
    product = db.query(Product).filter(Product.name == data["name"]).first()
    if product:
        for field, value in data.items():
            setattr(product, field, value)
        return product

    product = Product(**data)
    db.add(product)
    return product


def upsert_combo(db: Session, **data) -> Combo:
    combo = db.query(Combo).filter(Combo.name == data["name"]).first()
    if combo:
        for field, value in data.items():
            setattr(combo, field, value)
        return combo

    combo = Combo(**data)
    db.add(combo)
    return combo


def upsert_promotion(db: Session, **data) -> Promotion:
    promotion = db.query(Promotion).filter(Promotion.title == data["title"]).first()
    if promotion:
        for field, value in data.items():
            setattr(promotion, field, value)
        return promotion

    promotion = Promotion(**data)
    db.add(promotion)
    return promotion


def seed(db: Session):
    if not db.query(User).filter(User.email == "gerente@burgerhouse.com.br").first():
        db.add(User(
            name="Gerente Burger House",
            email="gerente@burgerhouse.com.br",
            password_hash=hash_password("Burger@123"),
            is_admin=True,
        ))

    categories = {
        "lanches": upsert_category(db, "Lanches", "lanches"),
        "combos": upsert_category(db, "Combos", "combos"),
        "acompanhamentos": upsert_category(db, "Acompanhamentos", "acompanhamentos"),
        "bebidas": upsert_category(db, "Bebidas", "bebidas"),
        "sobremesas": upsert_category(db, "Sobremesas", "sobremesas"),
    }

    for product in [
            dict(
                name="Classic Burger",
                description="Carne bovina 150g, queijo americano, alface, tomate, cebola caramelizada e maionese artesanal.",
                price=Decimal("28.90"),
                category_id=categories["lanches"].id,
                image_url="images/burger-classic.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Bacon Supreme",
                description="Dupla de carne 180g, bacon crocante, cheddar derretido, picles e molho barbecue defumado.",
                price=Decimal("38.90"),
                category_id=categories["lanches"].id,
                image_url="images/burger-bacon.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Cheddar Melt",
                description="Burger suculento com cheddar cremoso, cebola crispy, picles e molho especial da casa.",
                price=Decimal("34.90"),
                category_id=categories["lanches"].id,
                image_url="images/burger-classic.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Double Smash",
                description="Duas carnes smash 90g, dois queijos, pickles especiais, cebola e molho secret da casa.",
                price=Decimal("42.90"),
                category_id=categories["lanches"].id,
                image_url="images/burger-smash.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Chicken Crispy",
                description="Frango empanado crocante, queijo, alface, tomate e maionese levemente picante.",
                price=Decimal("31.90"),
                category_id=categories["lanches"].id,
                image_url="images/burger-classic.svg",
                is_active=True,
                is_available=False,
            ),
            dict(
                name="Veggie Burger",
                description="Burger vegetal grelhado, queijo, salada fresca, cebola roxa e molho de ervas.",
                price=Decimal("33.90"),
                category_id=categories["lanches"].id,
                image_url="images/burger-classic.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Batata Frita",
                description="Batata sequinha e crocante, finalizada com sal da casa.",
                price=Decimal("14.90"),
                category_id=categories["acompanhamentos"].id,
                image_url="images/gallery-grill.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Batata com Cheddar e Bacon",
                description="Batata frita coberta com cheddar cremoso e bacon crocante.",
                price=Decimal("22.90"),
                category_id=categories["acompanhamentos"].id,
                image_url="images/combo-house.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Onion Rings",
                description="Anéis de cebola empanados, dourados e crocantes.",
                price=Decimal("18.90"),
                category_id=categories["acompanhamentos"].id,
                image_url="images/gallery-grill.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Nuggets",
                description="Porção de nuggets crocantes com molho especial da casa.",
                price=Decimal("19.90"),
                category_id=categories["acompanhamentos"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Coca-Cola 350ml",
                description="Refrigerante gelado lata 350ml.",
                price=Decimal("7.90"),
                category_id=categories["bebidas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Guaraná 350ml",
                description="Guaraná gelado lata 350ml.",
                price=Decimal("7.90"),
                category_id=categories["bebidas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Suco Natural",
                description="Suco natural preparado na hora com frutas selecionadas.",
                price=Decimal("11.90"),
                category_id=categories["bebidas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Água Mineral",
                description="Água mineral sem gás, garrafa 500ml.",
                price=Decimal("5.90"),
                category_id=categories["bebidas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Brownie",
                description="Brownie de chocolate intenso com casquinha crocante.",
                price=Decimal("16.90"),
                category_id=categories["sobremesas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Milkshake",
                description="Milkshake cremoso de baunilha, chocolate ou morango.",
                price=Decimal("19.90"),
                category_id=categories["sobremesas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Pudim",
                description="Pudim artesanal com calda de caramelo.",
                price=Decimal("13.90"),
                category_id=categories["sobremesas"].id,
                image_url="images/gallery-restaurant.svg",
                is_active=True,
                is_available=True,
            ),
        ]:
        upsert_product(db, **product)

    for combo in [
            dict(
                name="Combo Classic",
                description="Classic Burger com batata frita e refrigerante 400ml.",
                items='["Classic Burger", "Batata Frita", "Refrigerante 400ml"]',
                price=Decimal("39.90"),
                image_url="images/combo-house.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Combo Bacon",
                description="Bacon Supreme com batata rústica e refrigerante 400ml.",
                items='["Bacon Supreme", "Batata Rústica", "Refrigerante 400ml"]',
                price=Decimal("52.90"),
                image_url="images/combo-house.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Combo Double",
                description="Double Smash com batata cheddar bacon e refrigerante 400ml.",
                items='["Double Smash", "Batata Cheddar Bacon", "Refrigerante 400ml"]',
                price=Decimal("57.90"),
                image_url="images/combo-house.svg",
                is_active=True,
                is_available=True,
            ),
            dict(
                name="Combo Família",
                description="Dois burgers, duas batatas e duas bebidas para dividir.",
                items='["2 Burgers", "2 Batatas", "2 Bebidas"]',
                price=Decimal("89.90"),
                image_url="images/combo-house.svg",
                is_active=True,
                is_available=True,
            ),
        ]:
        upsert_combo(db, **combo)

    for promotion in [
            dict(
                title="Terça do Smash",
                description="Na compra de dois Double Smash, a batata frita sai por conta da casa.",
                code="SMASHDAY",
                discount="Batata grátis",
                is_active=True,
            ),
            dict(
                title="Combo da Semana",
                description="Combo Classic com preço especial por tempo limitado.",
                code="HOUSE10",
                discount="10% OFF",
                is_active=True,
            ),
            dict(
                title="Festival Bacon Supreme",
                description="Bacon Supreme com Onion Rings por preço promocional durante o fim de semana.",
                code="BACON15",
                discount="15% OFF",
                is_active=True,
            ),
        ]:
        upsert_promotion(db, **promotion)

    db.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    database = SessionLocal()
    try:
        seed(database)
        print("Seed executado com sucesso.")
    finally:
        database.close()

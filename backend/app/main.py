from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Category, Combo, Product, Promotion, User
from app.routers import admin_router, auth_router, category_router, product_router
from app.seed import seed


app = FastAPI(title="Burger House API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Burger House API online"}


app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(category_router.router)
app.include_router(admin_router.router)

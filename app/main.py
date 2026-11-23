from contextlib import asynccontextmanager

from fastapi import FastAPI

from sqlalchemy import inspect

from app.api.routes.products import router as products_router
from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.models.product import ProductModel


def seed_initial_data():
    if not inspect(engine).has_table("products"):
        return

    db = SessionLocal()
    try:
        count = db.query(ProductModel).count()
        if count == 0:
            db.add_all(
                [
                    ProductModel(
                        name="Wireless Mouse",
                        description="Ergonomic wireless mouse with USB receiver",
                        price=29.99,
                    ),
                    ProductModel(
                        name="Mechanical Keyboard",
                        description="RGB backlit mechanical gaming keyboard",
                        price=89.50,
                    ),
                    ProductModel(
                        name="USB-C Hub",
                        description="7-in-1 USB-C adapter with 4K HDMI",
                        price=45.00,
                    ),
                ]
            )
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_initial_data()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(products_router)


@app.get("/health")
def health():
    return {"status": "ok"}

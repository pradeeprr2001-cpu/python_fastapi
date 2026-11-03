
from typing import List
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import os

# --- 1. DATABASE CONFIGURATION (PostgreSQL) ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:rwdy@localhost:5432/shop",  # local fallback
)

# Render gives "postgres://..." or "postgresql://...", but this project uses psycopg 3
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith(
    "postgresql+psycopg://"
):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Render Postgres requires SSL; skip this for local development
if "localhost" not in DATABASE_URL and "sslmode=" not in DATABASE_URL:
    joiner = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = f"{DATABASE_URL}{joiner}sslmode=require"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- 2. SQLALCHEMY MODEL ---
# Table Name: products
class ProductModel(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  description = Column(String, nullable=True)
  price = Column(Float)


# Create the database tables
Base.metadata.create_all(bind=engine)


# --- 3. PYDANTIC SCHEMAS ---
class ProductBase(BaseModel):
  name: str
  description: str | None = None
  price: float


class ProductCreate(ProductBase):
  pass


class ProductResponse(ProductBase):
  id: int

  class Config:
    from_attributes = True  # Pydantic v1 (use from_attributes = True on v2)


# Dependency to get DB session
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


# --- 4. STARTUP: SEED SAMPLE DATA ---
def seed_initial_data():
  db = SessionLocal()
  try:
    count = db.query(ProductModel).count()
    if count == 0:
      sample_products = [
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
      db.add_all(sample_products)
      db.commit()
  finally:
    db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
  seed_initial_data()  # runs on startup
  yield                # app runs here
  # code after yield would run on shutdown


# --- 5. FASTAPI APP & CRUD ENDPOINTS ---
app = FastAPI(
    title="Shop API - FastAPI CRUD with PostgreSQL", lifespan=lifespan
)


# CREATE
@app.post(
    "/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
  db_product = ProductModel(
      name=product.name, description=product.description, price=product.price
  )
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product


# READ (All)
@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
  products = db.query(ProductModel).offset(skip).limit(limit).all()
  return products


# READ (One)
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
  product = (
      db.query(ProductModel).filter(ProductModel.id == product_id).first()
  )
  if product is None:
    raise HTTPException(status_code=404, detail="Product not found")
  return product


# UPDATE
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, updated_product: ProductCreate, db: Session = Depends(get_db)
):
  product_query = db.query(ProductModel).filter(ProductModel.id == product_id)
  product = product_query.first()

  if product is None:
    raise HTTPException(status_code=404, detail="Product not found")

  product_query.update(updated_product.model_dump(), synchronize_session=False)
  db.commit()
  return product_query.first()


# DELETE
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
  product = (
      db.query(ProductModel).filter(ProductModel.id == product_id).first()
  )
  if product is None:
    raise HTTPException(status_code=404, detail="Product not found")

  db.delete(product)
  db.commit()
  return None
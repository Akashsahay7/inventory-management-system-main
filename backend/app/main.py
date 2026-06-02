from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models
from . import schemas
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Inventory API Running"}


# ==========================
# PRODUCTS
# ==========================

@app.post("/products")
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db, product)


@app.get("/products")
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(models.Product).all()


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_product(db, product_id)


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_product(
        db,
        product_id,
        product
    )


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_product(
        db,
        product_id
    )


# ==========================
# CUSTOMERS
# ==========================

@app.post("/customers")
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    return crud.create_customer(
        db,
        customer
    )


@app.get("/customers")
def get_customers(
    db: Session = Depends(get_db)
):
    return db.query(models.Customer).all()


@app.get("/customers/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_customer(
        db,
        customer_id
    )


@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_customer(
        db,
        customer_id
    )


# ==========================
# ORDERS
# ==========================

@app.post("/orders")
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    return crud.create_order(
        db,
        order
    )


@app.get("/orders")
def get_orders(
    db: Session = Depends(get_db)
):
    return db.query(models.Order).all()


@app.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_order(
        db,
        order_id
    )


@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_order(
        db,
        order_id
    )


# ==========================
# DASHBOARD
# ==========================

@app.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):
    total_products = db.query(models.Product).count()

    total_customers = db.query(models.Customer).count()

    total_orders = db.query(models.Order).count()

    low_stock_products = db.query(models.Product).filter(
        models.Product.quantity < 5
    ).count()

    return {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "low_stock_products": low_stock_products
    }
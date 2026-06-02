from pydantic import BaseModel, EmailStr
from typing import Optional


# ---------------- PRODUCTS ----------------

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


# ---------------- CUSTOMERS ----------------

class CustomerCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str


# ---------------- ORDERS ----------------

class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
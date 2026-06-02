from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Product, Customer, Order


# ==========================
# PRODUCTS
# ==========================

def create_product(db: Session, product):

    existing = db.query(Product).filter(
        Product.sku == product.sku
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    if product.quantity < 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    db_product = Product(
        name=product.name,
        sku=product.sku,
        price=product.price,
        quantity=product.quantity
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_product(db: Session, product_id: int):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def update_product(db: Session, product_id: int, product_data):

    product = get_product(db, product_id)

    for key, value in product_data.dict(
        exclude_unset=True
    ).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: int):

    product = get_product(db, product_id)

    existing_orders = db.query(Order).filter(
        Order.product_id == product_id
    ).first()

    if existing_orders:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product with existing orders"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted"
    }


# ==========================
# CUSTOMERS
# ==========================

def create_customer(db: Session, customer):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    db_customer = Customer(
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_customer(db: Session, customer_id: int):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


def delete_customer(db: Session, customer_id: int):

    customer = get_customer(db, customer_id)

    existing_orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).first()

    if existing_orders:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete customer with existing orders"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted"
    }


# ==========================
# ORDERS
# ==========================

def create_order(db: Session, order):

    product = db.query(Product).filter(
        Product.id == order.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    customer = db.query(Customer).filter(
        Customer.id == order.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if product.quantity < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_amount = product.price * order.quantity

    product.quantity -= order.quantity

    db_order = Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount
    )

    db.add(db_order)

    db.commit()

    db.refresh(db_order)

    return db_order


def get_order(db: Session, order_id: int):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


def delete_order(db: Session, order_id: int):

    order = get_order(db, order_id)

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted"
    }
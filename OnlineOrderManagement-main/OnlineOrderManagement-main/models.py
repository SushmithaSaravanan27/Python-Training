from dataclasses import dataclass

@dataclass
class Customer:
    name: str
    email: str

@dataclass
class Product:
    product_name: str
    price: float
    stock: int

@dataclass
class OrderItem:
    product_id: int
    quantity: int
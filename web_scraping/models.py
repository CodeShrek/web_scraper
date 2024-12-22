from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    name: str
    price: float
    original_price: float
    discount: float
    best_seller_rank: int
    ship_from: str
    sold_by: str
    rating: float
    description: str
    monthly_purchases: int
    category: str
    images: List[str]
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price,
            "original_price": self.original_price,
            "discount": self.discount,
            "best_seller_rank": self.best_seller_rank,
            "ship_from": self.ship_from,
            "sold_by": self.sold_by,
            "rating": self.rating,
            "description": self.description,
            "monthly_purchases": self.monthly_purchases,
            "category": self.category,
            "images": self.images
        } 
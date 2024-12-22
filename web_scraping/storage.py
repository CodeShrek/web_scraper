import json
import csv
from typing import List
from models import Product

class DataStorage:
    @staticmethod
    def save_to_json(products: List[Product], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in products], f, indent=4)
            
    @staticmethod
    def save_to_csv(products: List[Product], filename: str):
        if not products:
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=products[0].to_dict().keys())
            writer.writeheader()
            for product in products:
                writer.writerow(product.to_dict()) 
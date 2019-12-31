from pymongo import MongoClient
import os
import base64
from .description import product_description

class Shop:

    def __init__(self, storage):
        self.storage = storage

    '''
    @staticmethod
    def storage():
        myclient = MongoClient(
            f"mongodb+srv://{os.getenv('DB_NAME')}:{os.getenv('PASS')}@cluster0-twyu7.mongodb.net/test?retryWrites=true&w=majority")
        storage = myclient["Shop_db"]
        return storage
    '''

    def products_db(self):
        return self.storage["products"]

    def orders_db(self):
        return self.storage["orders"]

    def cart_db(self):
        return self.storage["carts"]

    def add_product_to_db(self, name, price, description=None, category="phone", image_path=None):
        if price <= 0:
            raise ValueError
        if not description:
            description = product_description(name)
        encoded_file = self.image_file_encode(image_path)
        db = self.products_db()
        db.insert_one({"category": category, "name": name, "price": price, "description": description,
                       "image_file": encoded_file})

    @staticmethod
    def image_file_encode(image_path=None):
        if image_path:
            with open(image_path, "rb") as myfile:
                data = myfile.read()
                return base64.b64encode(data)

    def add_product_to_cart(self, user_id, product_id, quantity):
        if quantity < 0:
            raise ValueError
        self.cart_db().update_one({"user_id": user_id}, {"$push": {"products": [product_id, quantity]}}, upsert=True)

    def buy_products_from_cart(self, user_id, delivery_price):
        cart_products = self.cart_db().find({"user_id": user_id}).next()["products"]
        order_amount = sum([self.products_db().find({"_id": x[0]}).next()["price"] * x[1] for x in cart_products]) + (
            delivery_price)
        self.orders_db().insert_one({"user_id": user_id, "products": cart_products, "order_amount": order_amount})
        self.cart_db().delete_one({"user_id": user_id})

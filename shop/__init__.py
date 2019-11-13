from pymongo import MongoClient
import os
import base64


class Shop:
    def shop_db(self):
        myclient = MongoClient(
            f"mongodb+srv://{os.getenv('DB_NAME')}:{os.getenv('PASS')}@cluster0-twyu7.mongodb.net/test?retryWrites=true&w=majority")
        shop_db = myclient["Shop_db"]
        return shop_db

    def products_db(self):
        shop_db = self.shop_db()
        products = shop_db["products"]
        return products

    def cart_db(self):
        shop_db = self.shop_db()
        carts = shop_db["carts"]
        return carts

    def add_poduct_to_db(self, name, price, description, category="phone", image_path="1.jpg"):
        encoded_file = self.image_file_encode(image_path)
        db = self.products_db()
        db.insert_one({"category": category, "name": name, "price": price, "description": description, "image_file": encoded_file})
    @staticmethod
    def image_file_encode(image_path="1.jpg"):
        with open(image_path, "rb") as myfile:
            data = myfile.read()
            return base64.b64encode(data)

    def add_product_to_cart(self, user_id, product_id, quantity):
        self.cart_db().update_one({"user_id": user_id}, {"$push": {"products": [product_id, quantity]}}, upsert=True)
from pymongo import MongoClient
import os
import base64

class Shop:
    def products_db(self):
        myclient = MongoClient(
            f"mongodb+srv://{os.getenv('DB_NAME')}:{os.getenv('PASS')}@cluster0-twyu7.mongodb.net/test?retryWrites=true&w=majority")
        shop_db = myclient["Shop_db"]
        products = shop_db["products"]
        return products


    def add_poduct_to_db(self,name,description, category="phone" ,image_path="1.jpg"):
        encoded_file = self.image_file_encode(image_path)
        db = self.products_db()
        db.insert_one({"category": category, "name": name, "description": description, "image_file": encoded_file})


    def image_file_encode(self, image_path="1.jpg"):
        with open(image_path, "rb") as myfile:
            data = myfile.read()
            return base64.b64encode(data)



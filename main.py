import pytest
from pymongo import MongoClient
import os
import base64
myclient = MongoClient(
            f"mongodb+srv://{os.getenv('DB_NAME')}:{os.getenv('PASS')}@cluster0-twyu7.mongodb.net/test?retryWrites=true&w=majority")
storage = myclient["Shop_db"]
from shop import Shop
shop = Shop(storage)
products = shop.products_db()
carts_db = shop.cart_db()
orders_db = shop.orders_db()





product_id = products.find({}).next()["_id"]
#shop.add_product_to_cart(1,product_id,2)



shop.buy_products_from_cart(1,22)

#shop.buy_products_from_cart(22, 1)


#pytest.main(['-s'])

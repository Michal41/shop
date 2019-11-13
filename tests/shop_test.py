import pytest
from pymongo import MongoClient
from shop import Shop
from pymongo import cursor
import base64


def test_shop_can_be_init():
    assert isinstance(Shop(), Shop)


def test_shop_db():
    try:
        products = Shop().products_db()
        products.insert_one({"123": "123"})
        products.delete_one({"123": "123"})
        assert 1
    except:
        assert 0


def test_shop_add_to_db():
    shop = Shop()
    products = shop.products_db()
    current_quantity = products.count_documents({"name": "samsung"})
    try:
        shop.add_poduct_to_db("samsung", 20, "S10")
        if not (products.count_documents({"name": "samsung"}) > current_quantity):
            raise SyntaxError
        products.delete_one({"name": "samsung", "description": "S10"})
        assert 1
    except SyntaxError:
        assert 0


def test_shop_image_file_encode():
    with open("1.jpg", "rb") as myfile:
        data = myfile.read()
    encoded = Shop().image_file_encode()
    assert base64.b64decode(encoded) == data

def test_shop_add_product_to_card():
    shop = Shop()
    carts = shop.cart_db()
    try:
        shop.add_product_to_cart(9876, 12344, 24)
        carts_length = len(carts.find({"user_id": 9876}).next()["products"])
        shop.add_product_to_cart(9876, 12344, 24)
        if not len(carts.find({"user_id": 9876}).next()["products"])>carts_length:
            raise AssertionError
        carts.delete_one({"user_id": 9876})
        assert True
    except AssertionError:
        assert False

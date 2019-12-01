import pytest
from pymongo import MongoClient
from shop import Shop
import os
import base64
from unittest.mock import Mock,patch,MagicMock,call


'''
myclient = MongoClient(
    f"mongodb+srv://{os.getenv('DB_NAME')}:{os.getenv('PASS')}@cluster0-twyu7.mongodb.net/test?retryWrites=true&w=majority")
storage = myclient["Shop_db"]
'''

def test_shop_can_be_init():
    mock = Mock()
    assert isinstance(Shop(mock), Shop)


def test_shop_add_to_db():
    mock = MagicMock()
    shop = Shop(mock)
    products = shop.products_db()
    shop.add_product_to_db("samsung", 12, "phonex")
    calls_args_list = products.insert_one.call_args_list
    expected = [call({'category': 'phone', 'name': 'samsung', 'price': 12, 'description': 'phonex', 'image_file': None})]
    assert expected == calls_args_list

def test_shop_add_to_db_negative_prinse():
    mock = MagicMock()
    with pytest.raises(ValueError):
        Shop(mock).add_product_to_db("name", -2, "description")

def test_shop_add_product_to_card():
    mock = MagicMock()
    shop = Shop(mock)
    carts = shop.cart_db()
    shop.add_product_to_cart(9876, 1234, 2)
    calls_args_list = carts.update_one.call_args_list
    expected_cal = [call({'user_id': 9876}, {'$push': {'products': [1234, 2]}}, upsert=True)]
    assert calls_args_list == expected_cal




def test_shop_add_product_to_card_negative_values():
    mock = MagicMock()
    with pytest.raises(ValueError):
        Shop(mock).add_product_to_cart(-1, -1, -1)

def test_shop_buy_products_from_cart():
    mock = MagicMock()
    shop = Shop(mock)
    orders = shop.orders_db()
    carts = shop.cart_db()
    shop.buy_products_from_cart(5, 22)
    insert_to_orders = orders.insert_one.call_args_list
    remove_from_carts = carts.delete_one.call_args_list
    assert insert_to_orders and remove_from_carts

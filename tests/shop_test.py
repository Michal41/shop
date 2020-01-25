import pytest
from shop import Shop
from unittest.mock import Mock, MagicMock, call
from shop.price_comparison import Price
from shop.report import Report

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


def test_shop_add_to_db_without_description():
    mock = MagicMock()
    shop = Shop(mock)
    products = shop.products_db()
    shop.add_product_to_db("samsung", 12)
    insert_to_products = products.insert_one.call_args_list
    assert insert_to_products


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


def test_price_list_validation():
    assert not(Price.price_list_validation([1, 100]))


def test_price_list_invalid_name():
    assert not(Price("xxxx", "xxxx").get_price_list())


def test_price_list_on_valid_name():
    assert (Price("xiomi redmi note 8").get_price_list())


def test_price_sugested_value():
    mock = MagicMock()
    price = Price(mock)
    price.get_price_list = MagicMock(return_value=[11, 1])
    assert price.get_sugested_price() == 6


def test_report_can_be_ininit():
    mock = Mock()
    assert isinstance(Report('a', 'asf', mock), Report)


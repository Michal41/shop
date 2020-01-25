import requests
import re


class Price:
    def __init__(self, name, category="phone"):
        self.name = name
        self.category = category

    def get_price_list(self):
        translate_category = {"phone": "smartfony-i-telefony-komorkowe-165",
                            "laptop": "laptopy-491",
                            "e-book reader": "czytniki-ebookow-76253?",
                            "tablet": "tablety-89253"}
        try:
            category = translate_category.get(self.category.lower())
            if not category:
                raise IndexError
            name = self.name.replace(" ", "%20")
            r = requests.get(f'https://allegro.pl/kategoria/{category}?string={name}&stan=nowe')
            price_list = [float(x.split("\"")[2]) for x in re.findall(r"amount.{25}", r.text)]
            if not(self.price_list_validation(price_list)):
                raise IndexError
            return price_list
        except IndexError:
            return []

    def get_sugested_price(self):
        price_list = self.get_price_list()
        return sum(price_list)//len(price_list) if price_list else 0

    def get_min_price(self):
        price_list = self.get_price_list()
        return min(price_list) if price_list else 0

    @classmethod
    def price_list_validation(cls, price_list):
        return max(price_list)/min(price_list) < 2.2



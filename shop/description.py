import requests
from bs4 import BeautifulSoup
import re


class Description:
    def __init__(self, product_name):
        self.product_name = product_name

    def get_product_description(self):
        product_name = re.sub(' +', ' ', self.product_name).replace(" ", "_")
        r = requests.get(f"https://en.wikipedia.org/w/index.php?search={product_name}")
        soup = BeautifulSoup(r.text, 'html.parser')
        result_list = soup.find_all("p")
        len_arr = [len(x) for x in result_list[:4]]
        if len_arr:
            result = result_list[len_arr.index(max(len_arr))]
            return re.sub('<[^>]+>', '', str(result))

        return ""



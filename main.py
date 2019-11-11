import pytest
from pymongo import MongoClient
import os
import base64

with open ("1.jpg", "rb") as myfile:
    data = myfile.read()
    print(len(data))
    print(len(base64.b64encode(data)))





import shop
print(len(list(*shop.Shop().products_db().find({"name": "phone"}))))




pytest.main()

import re
import uuid
import requests
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store

__author__ = 'ishween'


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(self.url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)


    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        #print(content)
        soup = BeautifulSoup(content, "html.parser")
        #print(soup)
        element = soup.find(self.tag_name, self.query)
        print(self.tag_name)
        print(self.query)
        string_price = element.text.strip()#it didn't took 1,330 as price look into it

        pattern = re.compile("(\d+.\d+)") #$155.00
        match = pattern.search(string_price)

        group = match.group()
        self.price = (float)(''.join(group[0:].split(',')))

        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id':self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id":item_id}))


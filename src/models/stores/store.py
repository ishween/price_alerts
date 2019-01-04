import uuid
import src.models.stores.constants as StoreConstants
from src.common.database import Database
import src.models.stores.errors as StoreErrors

__author__ = 'ishween'


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{"_id":_id}))

    def json(self):
        return {
            "_id" : self._id,
            "name" : self.name,
            "url_prefix" : self.url_prefix,
            "tag_name" : self.tag_name,
            "query" : self.query
        }

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id":self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name":store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        http://wwww.johnlewis -> http://www.johnlewis.com
        :param url_prefix:
        :return:
        """
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        """
        Return a stores from url which is entire url
        :param url: complete url and not just url_prefix
        :return: a stores , or raises a stores not found exception if no stores matches the url
        """
        for i in range(0, len(url)+1):
            try:
                store = cls.get_by_url_prefix(url[:i])  #slicing the url to match h, ht, htt, http... and so on
                return store
            except:
                raise StoreErrors.StoreNotFoundError("The URL Prefix used to find the stores didn't give us any result!")
                #return None # we can even write pass python automatically returns None

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.delete(StoreConstants.COLLECTION, {'_id':self._id})

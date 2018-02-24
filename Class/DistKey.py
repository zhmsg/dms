#! /usr/bin/env python
# coding: utf-8

from time import time
from bson.objectid import ObjectId
from pymongo import MongoClient, DESCENDING, ReturnDocument

__author__ = 'meisanggou'


class DistKey(object):

    def __init__(self, mongo_host):
        self.conn = MongoClient(mongo_host)
        self.db = self.conn.dms
        self.col = self.db.dk
        pass

    def insert(self, app, deadline, user_name, **kwargs):
        doc = kwargs
        doc.update(dict(app=app, deadline=deadline, user_name=user_name, insert_time=int(time())))
        self.col.insert_one(doc)
        pass

    def select(self, app, **kwargs):
        where_value = dict(app=app)
        where_value.update(kwargs)
        items = []
        for item in self.col.find(filter=where_value, sort=[("deadline", DESCENDING)]):
            item["_id"] = str(item["_id"])
            items.append(item)
        return items

    def select2(self, user_name, **kwargs):
        where_value = kwargs
        where_value.update(user_name=user_name)
        items = []
        for item in self.col.find(filter=where_value):
            item["id"] = str(item["_id"])
            del item["_id"]
            items.append(item)
        return items

    def select_secret(self, key_id, user_name, key):
        where_value = dict(_id=ObjectId(key_id), user_name=user_name)
        item = self.col.find_one(filter=where_value)
        if item is None:
            return None
        if key not in item:
            return None
        return item[key]

    def remove(self, doc_id):
        return self.col.delete_one({"_id": ObjectId(doc_id), "deadline": {"$lt": time()}})

    def update(self, doc_id, user_name, **kwargs):
        kwargs.pop("_id", None)
        kwargs.pop("user_name", None)
        kwargs.pop("deadline", None)
        r = self.col.update_one(filter={"_id": ObjectId(doc_id), "user_name": user_name}, update={'$set': kwargs})
        return r

    def update_deadline(self, doc_id, user_name, offset=None, deadline=None):
        if offset is not None:
            update_v = {'$inc': {"deadline": offset}}
        elif deadline is not None:
            update_v = {'$set': {"deadline": deadline}}
        else:
            return None
        return self.col.find_one_and_update(filter={"_id": ObjectId(doc_id), "user_name": user_name},
                                            update=update_v, return_document=ReturnDocument.AFTER)


if __name__ == "__main__":
    dt = DistKey("192.168.120.10")
    dt.insert("oss", int(time()) + 3600, "zh_test", key="abcdef")
    dt.select("oss")
    dt.remove("59c859c888874513883a41b9")

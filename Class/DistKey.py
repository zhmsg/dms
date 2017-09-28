#! /usr/bin/env python
# coding: utf-8

from time import time
from bson.objectid import ObjectId
from pymongo import MongoClient

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
        for item in self.col.find(filter=where_value):
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

    def remove(self, id):
        print self.col.delete_one({"_id": ObjectId(id)})


if __name__ == "__main__":
    dt = DistKey("192.168.120.10")
    dt.insert("oss", int(time()) + 3600, "zh_test", key="abcdef")
    dt.select("oss")
    dt.remove("59c859c888874513883a41b9")

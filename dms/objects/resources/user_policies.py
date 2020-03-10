#! /usr/bin/env python
# coding: utf-8
from pymongo import MongoClient

from dms.objects.resources.base import ResourceManager


__author__ = 'zhouhenglc'


class UserPoliciesManager(ResourceManager):
    NAME = "user_role"
    REQUIRED_CONFIG = ['mongo_host', 'mongo_user', 'mongo_password']

    def __init__(self):
        ResourceManager.__init__(self)
        mongo_host = self.config()['mongo_host']
        mongo_user = self.config()['mongo_user']
        mongo_password = self.config()['mongo_password']
        self.conn = MongoClient(mongo_host, username=mongo_user,
                                password=mongo_password)
        self.db = self.conn.dms
        self.col = self.db.user_policies

    def select_policies(self, user_name):
        role_v = self.col.find_one(dict(user_name=user_name))
        return role_v

    def get_policies(self, user_name):
        p = self.select_policies(user_name)
        if not p:
            return {}
        return p['policies']

    def new_policies(self, user_name, policies):
        if self.select_policies(user_name):
            return self.update_policies(user_name, policies)
        else:
            return self._insert(user_name, policies)

    def _insert(self, user_name, policies):
        data = {'user_name': user_name, 'policies': policies}
        self.col.insert_one(data)
        return data

    def update_policies(self, user_name, policies):
        data = {'policies': policies}
        self.col.update_one({'user_name': user_name}, {'$set': data})
        return policies

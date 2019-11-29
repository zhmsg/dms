#! /usr/bin/env python
# coding: utf-8
import time

from dms.utils.singleton import Singleton

from dms.objects.base import DBObject


class WebConfig(Singleton, DBObject):

    def __init__(self):
        DBObject.__init__(self)
        self.t = "web_config"
        self.cache = dict()
        self.cols = ["config_key", "config_value", "allow_update",
                     "update_time", "add_time"]

    def insert_config(self, config_key, config_value, allow_update=False):
        c_time = time.time()
        kwargs = dict(config_key=config_key, config_value=config_value,
                      allow_update=allow_update, update_time=c_time,
                      add_time=c_time)
        line = self.db.execute_insert(self.t, kwargs, ignore=True)
        if line > 0 and allow_update is False:
            self.cache[config_key] = kwargs
        return line

    def get_key(self, config_key):
        if config_key in self.cache:
            return self.cache[config_key]
        where_value = dict(config_key=config_key)
        items = self.db.execute_select(self.t, cols=self.cols,
                                       where_value=where_value)
        if len(items) <= 0:
            return None
        item = items[0]
        if item["allow_update"] is False:
            self.cache[config_key] = item
        return item

    def get_keys(self, config_keys):
        r = dict()
        for key in config_keys:
            r[key] = self.get_key(key)
        return r

    def update_key(self, config_key, config_value, allow_update=None):
        c_time = time.time()
        where_value = dict(config_key=config_key, allow_update=True)
        update_value = dict(config_value=config_value,  update_time=c_time)
        if allow_update is not None:
            update_value["allow_update"] = allow_update
        line = self.db.execute_update(self.t, update_value=update_value,
                                      where_value=where_value)
        return line

    def new_configs(self, configs, allow_update=False):
        for key, value in configs.items():
            self.insert_config(key, value, allow_update)
        return True

if __name__ == "__main__":
    config_man = WebConfig()
    config_man2 = WebConfig()
    print(id(config_man))
    print(id(config_man2))

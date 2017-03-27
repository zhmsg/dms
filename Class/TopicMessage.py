#! /usr/bin/env python
# coding: utf-8

from time import time
from Tools.Mysql_db import DB

__author__ = 'ZhouHeng'


class MessageManager(object):
    def __init__(self):
        self.db = DB()
        self.t_msg = "topic_message_content"
        self.t_user_tag = "user_topic_tag"

    def insert_topic_message(self, **kwargs):
        kwargs["insert_time"] = int(time())
        l = self.db.execute_insert(self.t_msg, args=kwargs)
        return l

    def insert_user_tag(self, **kwargs):
        kwargs["update_time"] = kwargs["insert_time"] = time()
        l = self.db.execute_insert(self.t_user_tag, args=kwargs, ignore=True)
        return l

    def update_user_tag(self, message_tag, user_name, **kwargs):
        where_value = dict(message_tag=message_tag, user_name=user_name)
        l = self.db.execute_update(self.t_user_tag, update_value=kwargs, where_value=where_value)
        return l

    def select_user_tag(self, message_tag=None):
        if message_tag is not None:
            where_value = dict(message_tag=message_tag)
        else:
            where_value = None
        cols = ["message_tag", "user_name", "notify_mode", "access_ding", "interval_time", "insert_time", "update_time"]
        db_items = self.db.execute_select(self.t_user_tag, where_value=where_value, cols=cols)
        return db_items

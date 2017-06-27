#! /usr/bin/env python
# coding: utf-8

from time import time
from Tools.Mysql_db import DB

__author__ = 'meisanggou'


class LinkManager(object):
    def __init__(self):
        self.db = DB()
        self.t_s = "short_link_s"
        self.t_n = "short_link_n"

    def insert_link(self, remark, link, adder, s=None):
        insert_time = time()
        kwargs = dict(remark=remark, link=link, adder=adder, insert_time=insert_time)
        t = self.t_n
        if s is not None:
            kwargs["s"] = s
            t = self.t_s
        l = self.db.execute_insert(t, kwargs, ignore=True)
        return l

    def select_link_s(self, s=None):
        cols = ["s", "remark", "link", "adder", "insert_time"]
        where_value = dict()
        if s is not None:
            where_value["s"] = s
        db_items = self.db.execute_select(self.t_s, where_value=where_value, cols=cols, package=True)
        return True, db_items

    def select_link_n(self, no=None):
        cols = ["no", "remark", "link", "adder", "insert_time"]
        where_value = dict()
        if no is not None:
            where_value["no"] = no
        db_items = self.db.execute_select(self.t_n, where_value=where_value, cols=cols, package=True)
        return True, db_items

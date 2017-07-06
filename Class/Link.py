#! /usr/bin/env python
# coding: utf-8

import hashlib
from time import time
from Tools.Mysql_db import DB

__author__ = 'meisanggou'


class LinkManager(object):
    def __init__(self):
        self.db = DB()
        self.t_s = "short_link_s"
        self.t_n = "short_link_n"
        self.t_m = "short_link_md5"

    def insert_md5(self, link_md5, s):
        kwargs = dict(link_md5=link_md5, s=s)
        l = self.db.execute_insert(self.t_m, kwargs, ignore=True)
        return l

    def select_md5(self, link_md5=None):
        cols = ["link_md5", "s"]
        where_value = dict()
        if link_md5 is not None:
            where_value["link_md5"] = link_md5
        db_items = self.db.execute_select(self.t_m, where_value=where_value, cols=cols)
        return True, db_items

    def query_md5(self, link):
        m = hashlib.md5()
        m.update(link)
        link_md5 = m.hexdigest().upper()
        exec_r, db_items = self.select_md5(link_md5)
        return exec_r, db_items

    def insert_link(self, remark, link, adder, s=None):
        m = hashlib.md5()
        m.update(link)
        link_md5 = m.hexdigest().upper()
        exec_r, db_items = self.select_md5(link_md5)
        if exec_r is False:
            return False, db_items
        if len(db_items) > 0:
            return True, db_items[0]["s"]
        insert_time = time()
        kwargs = dict(remark=remark[:200], link=link, link_md5=link_md5, adder=adder, insert_time=insert_time)
        t = self.t_n
        if s is not None:
            kwargs["s"] = s
            t = self.t_s
        l = self.db.execute_insert(t, kwargs, ignore=True)
        if s is None:
            exec_r, db_items = self.select_link_n(link_md5=link_md5)
            if len(db_items) == 0:
                return 0
            else:
                s = db_items[0]["no"]
        self.insert_md5(link_md5, s)
        return True, s

    def select_link_s(self, s=None):
        cols = ["s", "remark", "link", "adder", "insert_time"]
        where_value = dict()
        if s is not None:
            where_value["s"] = s
        db_items = self.db.execute_select(self.t_s, where_value=where_value, cols=cols, package=True)
        return True, db_items

    def select_link_n(self, no=None, link_md5=None):
        cols = ["no", "remark", "link", "adder", "insert_time"]
        where_value = dict()
        if no is not None:
            where_value["no"] = no
        if link_md5 is not None:
            where_value["link_md5"] = link_md5
        db_items = self.db.execute_select(self.t_n, where_value=where_value, cols=cols, package=True)
        return True, db_items


if __name__ == "__main__":
    l_man = LinkManager()
    s = l_man.insert_link("test", "http://dms.gene.ac/article/?action=look&article_no=18c1ed7251a911e7873f00163e0045ef",
                          "zh_test")
    print(s)

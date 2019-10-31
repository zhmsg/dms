#! /usr/bin/env python
# coding: utf-8

import os
from time import time

from dms.objects.base import DBObject

__author__ = 'ZhouHeng'


class IPManager(DBObject):

    def __init__(self):
        DBObject.__init__(self)
        self.ip_info = "ip_info_s"
        self.t_group = "ip_group"

    def select_info_info(self, ip_value):
        if type(ip_value) != int:
            return False, "Bad ip value"
        cols = ["ip_value_s", "ip_value_e", "info1", "info2"]
        where_cond = ["ip_value_s<=%s"]
        where_cond_args = [ip_value]
        l = self.db.execute_select(self.ip_info, cols=cols, where_cond=where_cond, where_cond_args=where_cond_args,
                                   order_by=["ip_value_s"], order_desc=True, limit=1, package=False)
        if l <= 0:
            return True, {"ip": ip_value, "info1": "", "info2": ""}
        s_ip, e_ip, info1, info2 = self.db.fetchone()
        if ip_value > e_ip:
            info1 = ""
            info2 = ""
        return True, {"ip": ip_value, "info1": info1, "info2": info2}

    def select(self, g_name=None, ip_s=None):
        cols = ["g_name", "ip_s", "ip_e", "remark", "insert_time"]
        where_value = dict()
        if g_name is not None:
            where_value["g_name"] = g_name
            if ip_s is not None:
                where_value["ip_s"] = ip_s
        db_items = self.db.execute_select(self.t_group, cols=cols, where_value=where_value)
        return db_items

    def query(self, g_name, ip_value):
        where_value = dict(g_name=g_name)
        where_cond = ["ip_s <= %s", "ip_e >= %s"]
        where_cond_args = [ip_value, ip_value]
        cols = ["g_name", "ip_s", "ip_e", "remark", "insert_time"]
        db_items = self.db.execute_select(self.t_group, cols=cols, where_value=where_value, where_cond=where_cond,
                                          where_cond_args=where_cond_args)
        return db_items

    def update(self, g_name, ip_s, **kwargs):
        where_value = dict(g_name=g_name, ip_s=ip_s)
        l = self.db.execute_update(self.t_group, update_value=kwargs, where_value=where_value)
        return l

    def insert_one(self, g_name, ip_value):
        where_value = dict(g_name=g_name)
        where_cond = ["ip_s <= %s"]
        where_cond_args = [ip_value]
        cols = ["ip_s", "ip_e"]
        db_items = self.db.execute_select(self.t_group, cols=cols, where_value=where_value, where_cond=where_cond,
                                          where_cond_args=where_cond_args, order_by=["ip_s"], limit=1, order_desc=True)
        if len(db_items) <= 0:
            self.insert(g_name, ip_value, ip_value, '')
        else:
            item = db_items[0]
            if item["ip_e"] >= ip_value:
                return True
            elif item["ip_e"] + 1 == ip_value:
                self.update(g_name, item["ip_s"], ip_e=ip_value)
            else:
                self.insert(g_name, ip_value, ip_value, '')
        return True

    def insert(self, g_name, ip_s, ip_e, remark):
        items = self.select(g_name, ip_s)
        if len(items) > 0:
            item = items[0]
            if item["ip_e"] > ip_e:
                return item
            else:
                self.update(g_name, ip_s, ip_e=ip_e, remark=remark)
                item.update(ip_e=ip_e, remark=remark)
                return item
        kwargs = dict(g_name=g_name, ip_s=ip_s, ip_e=ip_e, remark=remark)
        kwargs.update(insert_time=int(time()))
        l = self.db.execute_insert(self.t_group, kwargs)
        return kwargs

    def delete(self, g_name, ip_s):
        where_value = dict(g_name=g_name, ip_s=ip_s)
        l = self.db.execute_delete(self.t_group, where_value=where_value)
        return l

if __name__ == "__main__":
    ip_man = IPManager()
    ip_man.insert_one("公司IP", 3232266250)
    ip_man.insert("公司IP", 3232266260, 3232266270, '192.168.120.20-192.168.120.30')
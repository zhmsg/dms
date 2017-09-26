#! /usr/bin/env python
# coding: utf-8

import os
from time import time
from JYTools.DB import DB
from Class import conf_dir

__author__ = 'ZhouHeng'


class IPManager(object):

    def __init__(self):
        self.db = DB(conf_path=os.path.join(conf_dir, "mysql_dms.conf"))
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

    def select(self, g_name=None):
        cols = ["g_name", "ip_s", "ip_e", "remark", "insert_time"]
        where_value = dict()
        if g_name is not None:
            where_value["g_name"] = g_name
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

    def insert(self, g_name, ip_s, ip_e, remark):
        kwargs = dict(g_name=g_name, ip_s=ip_s, ip_e=ip_e, remark=remark)
        kwargs.update(insert_time=int(time()))
        l = self.db.execute_insert(self.t_group, kwargs)
        return kwargs

    def delete(self, g_name, ip_s):
        where_value = dict(g_name=g_name, ip_s=ip_s)
        l = self.db.execute_delete(self.t_group, where_value=where_value)
        return l

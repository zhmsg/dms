#! /usr/bin/env python
# coding: utf-8

import os
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
        pass

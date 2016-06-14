#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Tools.Mysql_db import DB


class IPManager:

    def __init__(self):
        self.db = DB()
        self.ip_info = "ip_info_s"

    def select_info_info(self, ip_value):
        if type(ip_value) != int:
            return False, "Bad ip value"
        select_sql = "SELECT ip_value_s,ip_value_e,info1,info2 FROM %s WHERE ip_value_s<%s ORDER BY ip_value_s DESC LIMIT 1;" \
                     % (self.ip_info, ip_value)
        result = self.db.execute(select_sql)
        if result <= 0:
            return True, {"ip": ip_value, "info1": "", "info2": ""}
        s_ip, e_ip, info1, info2 = self.db.fetchone()
        if ip_value > e_ip:
            info1 = ""
            info2 = ""
        return True, {"ip": ip_value, "info1": info1, "info2": info2}

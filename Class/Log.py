#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from datetime import timedelta
from time import time
from Class import env
from Check import check_int

__author__ = 'ZhouHeng'


class LogManager:

    def __init__(self):
        if env == "Development":
            service_mysql = "192.168.120.2"
        else:
            service_mysql = "rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com"
        self.db = DB(host=service_mysql, mysql_user="gener", mysql_password="gene_ac252", mysql_db="clinic")
        self.api_log = "api_log"
        self.log_cols = ["run_begin", "host", "url", "method", "account", "ip", "level", "info", "run_time"]
        self.log_level = ["error", "base_error", "bad_req", "http_error", "info"]

    def _select_log(self, where_sql):
        select_sql = "SELECT %s FROM %s WHERE %s" % (",".join(self.log_cols), self.api_log, where_sql)
        self.db.execute(select_sql)
        log_records = []
        for item in self.db.fetchall():
            log_item = {}
            for i in range(len(self.log_cols)):
                log_item[self.log_cols[i]] = item[i]
            log_records.insert(0, log_item)
        return True, log_records

    def show_log(self, hour, minute, second, look_before=False, level=None, search_url=""):
        if check_int(hour, 0, 24) is False:
            return False, "Bad hour"
        if check_int(minute, 0, 60) is False:
            return False, "Bad minute"
        if check_int(second, 0, 60) is False:
            return False, "Bad second"
        run_begin = time() - timedelta(hours=hour, minutes=minute, seconds=second).total_seconds()
        where_sql_list = ["run_begin>=%s " % run_begin]
        if look_before is False:
            where_sql_list.append("level <> 'before'")
        if level is not None:
            if level not in self.log_level:
                return False, "Bad level"
            where_sql_list.append("level = '%s'" % level)
        if search_url is not None and search_url != "":
            where_sql_list.append("url like '%s%%'" % search_url)
        where_sql = " AND ".join(where_sql_list)
        return self._select_log(where_sql)


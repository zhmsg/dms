#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from datetime import timedelta
from time import time
from Class import env
from Check import check_int, check_sql_character

__author__ = 'ZhouHeng'


class LogManager:

    def __init__(self):
        if env == "Development":
            service_mysql = "192.168.120.2"
        else:
            service_mysql = "rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com"
        self.db = DB(host=service_mysql, mysql_user="gener", mysql_password="gene_ac252", mysql_db="clinic")
        self.local_db = DB()
        self.api_log = "api_log"
        self.login_server = "login_server"
        self.log_cols = ["run_begin", "host", "url", "method", "account", "ip", "level", "info", "run_time"]
        self.log_level = ["error", "base_error", "bad_req", "http_error", "info"]

    def _select_log(self, where_sql):
        select_sql = "SELECT %s FROM %s WHERE %s ORDER BY log_no DESC LIMIT 250;" % (",".join(self.log_cols), self.api_log, where_sql)
        self.db.execute(select_sql)
        log_records = []
        for item in self.db.fetchall():
            log_item = {}
            for i in range(len(self.log_cols)):
                log_item[self.log_cols[i]] = item[i]
            log_records.append(log_item)
        return True, log_records

    def show_log(self, start_time=None, end_time=None, level=None, search_url="", search_account=""):
        run_end = time()
        run_begin = run_end - timedelta(hours=1).total_seconds()
        require = {}
        if start_time is not None and start_time > run_begin:
            run_begin = start_time
            require["start_time"] = start_time
        if end_time is not None and end_time < run_end:
            run_end = end_time
            require["end_time"] = end_time
        where_sql_list = ["run_begin>=%s " % run_begin, "run_begin<=%s " % run_end]
        if level is not None:
            if level not in self.log_level:
                return False, "Bad level"
            where_sql_list.append("level = '%s'" % level)
        if search_url is not None and search_url != "":
            search_url = check_sql_character(search_url)
            where_sql_list.append("url like '%s%%'" % search_url)
        if search_account is not None and search_account != "":
            search_account = check_sql_character(search_account)
            where_sql_list.append("account = '%s'" % search_account)
        where_sql = " AND ".join(where_sql_list)
        result, log_records = self._select_log(where_sql)
        if result is False:
            return log_records
        return True, {"log_records": log_records, "require": require}

    def insert_login_server(self, server_ip, server_name, user_ip, user_name, login_time):
        if check_int(server_ip, 1, sys.maxint) is False:
            return False, "Bad server ip"
        if check_int(user_ip, 1, sys.maxint) is False:
            return False, "Bad user ip"
        now_time = int(time())
        if check_int(login_time, now_time - 100, now_time + 100) is False:
            return False, "Bad login time"
        user_name = check_sql_character(user_name)[:50]
        server_name = check_sql_character(server_name)[:20]
        insert_sql = "INSERT INTO %s (server_ip,server_name,user_ip,user_name,login_time) VALUES (%s,'%s',%s,'%s',%s);" \
                     % (self.login_server, server_ip, server_name, user_ip, user_name, login_time)
        self.local_db.execute(insert_sql)
        return True, "success"

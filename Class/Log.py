#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from datetime import timedelta
from time import time
from Class import env
from Class.Task import TaskManager
from Check import check_int, check_sql_character

__author__ = 'ZhouHeng'


class LogManager:

    def __init__(self):
        if env == "Development":
            service_mysql = "192.168.120.2"
            self.data_db_name = "clinic_basic"
        else:
            service_mysql = "rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com"
            self.data_db_name = "clinic"
        self.db = DB(host=service_mysql, mysql_user="gener", mysql_password="gene_ac252", mysql_db=self.data_db_name)
        self.local_db = DB()
        self.api_log = "api_log_2"
        self.login_server = "login_server"
        self.log_cols = ["log_no", "run_begin", "host", "url", "method", "account", "ip", "level", "info", "run_time"]
        self.login_cols = ["login_no", "server_ip", "server_name", "user_ip", "user_name", "login_time"]
        self.log_level = ["error", "base_error", "bad_req", "http_error", "info"]
        self.log_task = TaskManager(1)
        self.login_task = TaskManager(2)
        self.basic_time = 1473350400  # 2016/09/09 00:00:00

    def _select_log(self, where_sql, limit_num=250):
        select_sql = "SELECT %s FROM %s WHERE %s ORDER BY log_no DESC LIMIT %s;" \
                     % (",".join(self.log_cols), self.api_log, where_sql, limit_num)
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
        where_sql_list = ["log_no>=%s " % long(run_begin * 10000), "log_no<=%s " % long(run_end * 10000)]
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
            return False, log_records
        return True, {"log_records": log_records, "require": require}

    def select_daily_log(self):
        result, info = self.log_task.select_scheduler_status()
        if result is False:
            return False, info
        if info["task_status"] is None:
            run_end = long(time() * 10000)
            run_begin = long(run_end - timedelta(days=1).total_seconds() * 10000)
            require = {"start_time": run_begin, "end_time": run_end}
            where_sql = "log_no >= %s AND log_no <= %s AND level <> 'info'" % (run_begin, run_end)
        else:
            log_no = long(info["task_status"])
            require = {"log_no": log_no}
            where_sql = "log_no > %s AND level <> 'info'" % log_no
        result, log_records = self._select_log(where_sql)
        if result is False:
            return False, log_records
        if len(log_records) > 0:
            self.log_task.update_scheduler_status(log_records[0]["log_no"], "system", "daily log")
        return True, {"log_records": log_records, "require": require}

    def register_daily_task(self):
        user_name = "system"
        reason = u"每日运行日志"
        reason_desc = u"每天8：30，将一天前到现在所有的不正确或者未正确执行的请求日志发送给相关权限人员。"
        task_no = (int(time()) - self.basic_time) / 86400
        return self.log_task.register_new_task(task_no, user_name=user_name, reason=reason, reason_desc=reason_desc)

    def _select_login(self, where_sql, limit_num=250):
        select_sql = "SELECT %s FROM %s WHERE %s ORDER BY login_no DESC LIMIT %s;" \
                     % (",".join(self.login_cols), self.login_server, where_sql, limit_num)
        self.local_db.execute(select_sql)
        login_records = []
        for item in self.local_db.fetchall():
            login_item = {}
            for i in range(len(self.login_cols)):
                login_item[self.login_cols[i]] = item[i]
            login_records.append(login_item)
        return True, login_records

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

    def select_login_log(self):
        result, info = self.login_task.select_scheduler_status()
        if result is False:
            return False, info
        if info["task_status"] is None:
            run_end = time()
            run_begin = run_end - timedelta(days=1).total_seconds()
            where_sql = "login_time >= %s AND login_time <= %s" % (run_begin, run_end)
        else:
            login_no = int(info["task_status"])
            where_sql = "login_no > %s" % login_no
        result, login_records = self._select_login(where_sql)
        if result is False:
            return False, login_records
        if len(login_records) > 0:
            self.login_task.update_scheduler_status(login_records[0]["login_no"], "system", "")
        return True, {"login_records": login_records}

    def register_login_task(self):
        user_name = "system"
        reason = u"登录记录"
        reason_desc = u"每天9-15点5分，将服务器登录记录送给相关权限人员。"
        task_no = (int(time()) - self.basic_time) / 3600
        return self.login_task.register_new_task(task_no, user_name=user_name, reason=reason, reason_desc=reason_desc)

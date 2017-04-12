#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.TimeUUID import TimeStampUUID2
from datetime import timedelta
from time import time
from Class import env
from Class.Task import TaskManager
from Check import check_int, check_sql_character

__author__ = 'ZhouHeng'

ts_uuid2 = TimeStampUUID2()


class LogManager(object):

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
        self.api_log_2 = "flask_run_log"
        self.login_server = "login_server"
        self.log_cols = ["log_no", "run_begin", "host", "url", "method", "account", "ip", "level", "info", "run_time"]
        self.log2_cols = ["log_no", "run_begin", "host", "url", "args", "method", "headers", "account", "resource_id",
                          "ip", "level", "info", "run_time"]
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

    def _select_log2(self, where_value, where_cond, where_cond_args, limit_num=250):
        log_records = self.db.execute_select(self.api_log_2, where_value=where_value, where_cond=where_cond,
                                             where_cond_args=where_cond_args, cols=self.log2_cols, limit=limit_num,
                                             order_by=["log_no"], order_desc=True)
        return log_records

    def select_log(self, log_no):
        where_sql = "log_no=%s" % long(log_no)
        return self._select_log(where_sql, limit_num=1)

    def show_log2(self, start_time=None, end_time=None, level=None, search_url="", search_account=""):
        run_end = time()
        run_begin = run_end - timedelta(hours=1).total_seconds()
        require = {}
        where_cond = []
        where_cond_args = []
        where_value = dict()
        if start_time is not None and start_time > run_begin:
            where_cond.append("log_no>=%s")
            where_cond_args.append(ts_uuid2.min_uuid(start_time))
            require["start_time"] = start_time
        if end_time is not None and end_time < run_end:
            where_cond.append("log_no<=%s")
            where_cond_args.append(ts_uuid2.max_uuid(end_time))
            require["end_time"] = end_time
        if level is not None:
            if level not in self.log_level:
                return False, "Bad level"
            where_value["level"] = level
        if search_url is not None and search_url != "":
            search_url = check_sql_character(search_url)
            where_cond.append("url LIKE %s")
            where_cond_args.append(search_url)
        if search_account is not None and search_account != "":
            where_value["account"] = search_account
        log_records = self._select_log2(where_value=where_value, where_cond=where_cond, where_cond_args=where_cond_args)
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

    def _select_login(self, where_sql=None, limit_num=250):
        if where_sql is not None:
            select_sql = "SELECT %s FROM %s WHERE %s ORDER BY login_no DESC LIMIT %s;" \
                         % (",".join(self.login_cols), self.login_server, where_sql, limit_num)
        else:
            select_sql = "SELECT %s FROM %s ORDER BY login_no DESC LIMIT %s;" \
                             % (",".join(self.login_cols), self.login_server, limit_num)
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

    def query_login_log(self, limit_num=20):
        result, login_records = self._select_login(limit_num=limit_num)
        if result is False:
            return False, login_records
        return True, {"login_records": login_records}

    def register_login_task(self):
        user_name = "system"
        reason = u"登录记录"
        reason_desc = u"每天9-15点5分，将服务器登录记录送给相关权限人员。"
        task_no = (int(time()) - self.basic_time) / 3600
        return self.login_task.register_new_task(task_no, user_name=user_name, reason=reason, reason_desc=reason_desc)

#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from datetime import datetime

__author__ = 'ZhouHeng'


class DataManager:

    def __init__(self):
        self.db = DB()
        self.data = "data_status"

    def new(self, inputuser):
        try:
            inputtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_sql = "INSERT INTO %s (inputtime,inputuser) VALUES ('%s','%s');" % (self.data, inputtime, inputuser)
            self.db.execute("LOCK TABLES %s WRITE;" % self.data)
            insert_result = self.db.execute(insert_sql)
            if insert_result != 1:
                self.db.execute("UNLOCK TABLES;")
                return False, u"新建记录失败，请重试"
            self.db.execute("SELECT MAX(data_no) FROM %s;" % self.data)
            data_no = self.db.fetchone()[0]
            self.db.execute("UNLOCK TABLES;")
            return True, data_no
        except Exception as e:
            self.db.execute("UNLOCK TABLES;")
            error_message = "%s" % str(e.args)
            return False, error_message

    def update(self, data_no, status):
        try:
            update_sql = "UPDATE %s SET status=%s WHERE data_no=%s;" % (self.data, status, data_no)
            result = self.db.execute(update_sql)
            if result <= 0:
                return False, u"数据编号不存在"
            return True, ""
        except Exception as e:
            error_message = "%s" % str(e.args)
            print(error_message)
            return False, error_message

    def get(self, data_no=-1):
        select_sql = "SELECT data_no, status, inputtime FROM %s " % self.data
        if data_no != -1:
            select_sql += "WHERE data_no=%s " % data_no
        select_sql += "ORDER BY inputtime DESC;"
        result = self.db.execute(select_sql)
        data_info =[]
        for item in self.db.fetchall():
            data_info.append({"data_no": item[0], "status": item[1], "inputtime": item[2]})
        return data_info


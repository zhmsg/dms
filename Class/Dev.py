#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.MyExcel import write_excel
from datetime import datetime
from Class import TIME_FORMAT_STR

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class DevManager:

    def __init__(self):
        self.db = DB()
        self.auth_role = "auth_role"
        self.operate_role = "operate_role"

    def get_operate_auth(self):
        try:
            select_sql = "SELECT module,operate,description,o.role FROM operate_auth AS o, auth_role AS r WHERE o.role=r.role " \
                     "ORDER BY module DESC, o.role;"
            self.db.execute(select_sql)
            operate_auth = []
            for item in self.db.fetchall():
                operate_auth.append({"module": item[0], "operate": item[1], "description": item[2], "role": item[3]})
            return True, operate_auth
        except Exception as e:
            error_message = str(e.args)
            print(error_message)
            return False, error_message

    def get_operate_auth_file(self):
        try:
            result, operate_auth = self.get_operate_auth()
            if result is False:
                return False, operate_auth
            operate_auth_array = []
            for item in operate_auth:
                operate_auth_array.append([item["module"], item["operate"], item["role"] + " " + item["description"]])
            titles = [u"模块", u"操作", u"拥有操作权限的角色"]
            file = "operate_auth_%s.xls" % datetime.now().strftime(TIME_FORMAT_STR)
            save_path = "%s/%s" % (temp_dir, file)
            print(save_path)
            write_result, message = write_excel(save_path, operate_auth_array, titles)
            if write_result is False:
                return write_result, message
            return True, {"DIR": temp_dir, "FILE": file}
        except Exception as e:
            error_message = str(e.args)
            print(error_message)
            return False, error_message
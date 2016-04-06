#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.MyExcel import write_excel
from Check import check_sql_character
from datetime import datetime
from time import time
from Class import TIME_FORMAT_STR

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class DevManager:

    def __init__(self):
        self.db = DB()
        service_mysql = "rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com"
        self.service_db = DB(host=service_mysql, mysql_user="gener", mysql_password="gene_ac252", mysql_db="information_schema")
        self.auth_role = "auth_role"
        self.operate_role = "operate_role"
        self.right_module = "right_module"
        self.right_module_role = "right_module_role"
        self.right_action_role = "right_action_role"

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
            write_result, message = write_excel(save_path, operate_auth_array, titles)
            if write_result is False:
                return write_result, message
            return True, {"DIR": temp_dir, "FILE": file}
        except Exception as e:
            error_message = str(e.args)
            print(error_message)
            return False, error_message

    def list_table(self):
        sql = "SELECT TABLE_NAME, CREATE_TIME,TABLE_COMMENT FROM TABLES WHERE TABLE_SCHEMA='clinic' AND TABLE_TYPE='BASE TABLE';"
        self.service_db.execute(sql)
        table_list = []
        for item in self.service_db.fetchall():
            table_list.append({"table_name": item[0], "create_time": item[1], "table_comment": item[2]})
        return True, table_list

    def get_table_info(self, table_name):
        sql = "SELECT COLUMN_NAME, COLUMN_TYPE,COLUMN_KEY,COLUMN_DEFAULT,EXTRA,COLUMN_COMMENT,IS_NULLABLE " \
              "FROM columns WHERE TABLE_NAME='%s';" % table_name
        self.service_db.execute(sql)
        column_info = []
        for item in self.service_db.fetchall():
            column_info.append({"column_name": item[0], "column_type": item[1], "column_key": item[2],
                                "column_default": item[3], "extra": item[4], "column_comment": item[5],
                                "is_nullable": item[6]})
        return True, column_info

    def get_right_module(self):
        select_item = ["module_no", "module_title", "module_desc"]
        select_sql = "SELECT %s FROM %s;" % (",".join(select_item), self.right_module)
        self.db.execute(select_sql)
        module_info = []
        for item in self.db.fetchall():
            info = {}
            for i in range(len(item)):
                info[select_item[i]] = item[i]
            module_info.append(info)
        return True, module_info

    def get_right_module_role(self, module_no):
        if type(module_no) != int:
            return False, "Bad module_no"
        select_item = ["module_no", "module_role", "role_desc"]
        select_sql = "SELECT %s FROM %s WHERE module_no=%s;" % (",".join(select_item), self.right_module_role, module_no)
        self.db.execute(select_sql)
        module_role_info = []
        for item in self.db.fetchall():
            info = {}
            for i in range(len(item)):
                info[select_item[i]] = item[i]
            module_role_info.append(info)
        return True, module_role_info

    def get_right_action_role(self, module_no):
        if type(module_no) != int:
            return False, "Bad module_no"
        select_item = ["action_no", "module_no", "action_desc", "min_role"]
        select_sql = "SELECT %s FROM %s WHERE module_no=%s;" % (",".join(select_item), self.right_action_role, module_no)
        self.db.execute(select_sql)
        action_role_info = []
        for item in self.db.fetchall():
            info = {}
            for i in range(len(item)):
                info[select_item[i]] = item[i]
            action_role_info.append(info)
        return True, action_role_info

    def new_right_action(self, module_no, action_desc, min_role, adder):
        add_time = int(time())
        action_desc = check_sql_character(action_desc)
        insert_sql = "INSERT INTO %s (module_no,action_desc,min_role,adder,add_time) VALUES (%s,'%s','%s','%s',%s)" \
                     % (self.right_action_role, module_no, action_desc, min_role[:1], adder, add_time)
        self.db.execute(insert_sql)
        return True, "success"

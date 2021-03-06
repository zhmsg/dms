#! /usr/bin/env python
# coding: utf-8

import sys
import re
import tempfile
from Tools.Mysql_db import DB
from .Check import check_sql_character
from time import time
from Class import env
from .Task import DayTaskManager

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class DevManager(object):

    def __init__(self):
        self.db = DB()
        if env == "Development":
            service_mysql = "172.16.110.4"
            self.data_db_name = "jingd_clinic"
            self.port = 9536
            self.user = "jingdr"
            self.password = "JingD1017@@g"
        else:
            service_mysql = "rdsikqm8sr3rugdu1muh3421.mysql.rds.aliyuncs.com"
            self.data_db_name = "clinic"
            self.port = 3306
            self.user = "gene_app_r"
            self.password = "APP_ac1711"
        self.service_db = DB(host=service_mysql, mysql_user=self.user, mysql_password=self.password,
                             mysql_db="information_schema", port=self.port)
        self.auth_role = "auth_role"
        self.operate_role = "operate_role"
        self.right_module = "right_module"
        self.right_module_role = "right_module_role"
        self.right_action_role = "right_action_role"
        self.t_backup = "backup_table"
        self.backup_task = DayTaskManager(5)

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

    def list_table(self):
        sql = "SELECT TABLE_NAME,CREATE_TIME,TABLE_COMMENT FROM TABLES WHERE TABLE_SCHEMA=%s AND TABLE_TYPE='BASE TABLE';"
        self.service_db.execute(sql, args=[self.data_db_name])
        table_list = []
        for item in self.service_db.fetchall():
            table_list.append({"table_name": item[0], "create_time": item[1], "table_comment": item[2]})
        return True, table_list

    def get_table_info(self, table_name):
        sql = "SELECT COLUMN_NAME, COLUMN_TYPE,COLUMN_KEY,COLUMN_DEFAULT,EXTRA,COLUMN_COMMENT,IS_NULLABLE " \
              "FROM columns WHERE TABLE_NAME=%s AND TABLE_SCHEMA=%s;"
        self.service_db.execute(sql, args=[table_name, self.data_db_name])
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
        select_item = ["action_no", "module_no", "action_desc", "min_role", "adder"]
        select_sql = "SELECT %s FROM %s WHERE module_no=%s AND is_delete=0 ORDER BY min_role;" \
                     % (",".join(select_item), self.right_action_role, module_no)
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

    def del_right_action(self, adder, action_no):
        del_time = int(time())
        delete_sql = "UPDATE %s SET is_delete=1,add_time=%s WHERE action_no=%s AND adder='%s';" \
                     % (self.right_action_role, del_time, action_no, adder)
        self.db.execute(delete_sql)
        return True, "success"

    def backup_table(self, t_name, sql_path):
        self.service_db.backup_table(t_name, sql_path, self.data_db_name)
        return True, sql_path

    def register_backup_task(self):
        user_name = "system"
        reason = "备份线上数据表"
        reason_desc = "每天0：30，备份线上数据表。"
        return self.backup_task.register_new_task(user_name=user_name, reason=reason, reason_desc=reason_desc)

    def select_backup_table(self):
        cols = ["t_name", "status", "adder", "insert_time"]
        db_items = self.db.execute_select(self.t_backup, cols=cols)
        return db_items

    def insert_backup_table(self, t_name, adder):
        insert_data = dict(t_name=t_name, adder=adder, status=0)
        insert_data["insert_time"] = int(time())
        l = self.db.execute_insert(self.t_backup, kwargs=insert_data, ignore=True)
        return l

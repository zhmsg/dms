#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Class import table_manager, TIME_FORMAT
from Check import check_chinese_en, check_http_method, check_path, check_sql_character, check_int, check_char, fill_zero
from Tools.Wx import WxManager

temp_dir = tempfile.gettempdir()
wx = WxManager()

__author__ = 'ZhouHeng'


class StatusManager:

    def __init__(self):
        self.db = DB()
        self.service_module = table_manager.service_module
        self.function_module = table_manager.function_module
        self.error_type = table_manager.error_type
        self.status_code = table_manager.status_code
        self.user = "sys_user"

    def new_status_code(self, service_id, fun_id, type_id, error_id, error_desc, adder):
        if check_int(service_id) is False:
            return "Bad service_id"
        if check_int(fun_id) is False:
            return "Bad fun_id"
        if check_int(type_id) is False:
            return "Bad type_id"
        if check_int(error_id) is False:
            return "Bad error_id"
        status_code = fill_zero(service_id, 2) + fill_zero(fun_id, 2) + fill_zero(type_id, 2) + fill_zero(error_id, 2)
        add_time = datetime.now().strftime(TIME_FORMAT)
        code_desc = check_sql_character(error_desc)
        insert_sql = "INSERT IGNORE INTO %s (status_code,code_desc,add_time,adder) " \
                     "VALUES (%s,'%s','%s','%s');" % (self.status_code, status_code, code_desc, add_time, adder)
        self.db.execute(insert_sql)
        return True, status_code

    def new_mul_status_code(self, service_id, fun_id, error_info, adder):
        if check_int(service_id) is False:
            return "Bad service_id"
        if check_int(fun_id) is False:
            return "Bad fun_id"

    def get_status_code(self):
        select_sql = "SELECT status_code,code_desc,add_time,adder FROM %s;" % self.status_code
        self.db.execute(select_sql)
        status_info = []
        for item in self.db.fetchall():
            status_info.append({"status_code": fill_zero(item[0], 8), "code_desc": item[1],
                                "add_time": item[2].strftime(TIME_FORMAT), "adder": item[3]})
        return True, status_info

    def get_function_info(self):
        select_sql = "SELECT service_id,service_title,service_desc FROM %s;" % self.service_module
        self.db.execute(select_sql)
        module_info = {}
        for item in self.db.fetchall():
            service_id_s = fill_zero(item[0], 2)
            module_info[service_id_s] = {"title": item[1], "desc": item[2], "fun_info": {}}
        select_sql = "SELECT service_id,function_id,function_title,function_desc FROM %s;" % self.function_module
        self.db.execute(select_sql)
        for item in self.db.fetchall():
            service_id_s = fill_zero(item[0], 2)
            if service_id_s in module_info:
                fun_id_s = fill_zero(item[1], 2)
                module_info[service_id_s]["fun_info"][fun_id_s] = {"title": item[2], "desc": item[3]}
        return True, module_info

    def get_error_type(self):
        select_sql = "SELECT type_id,type_title,type_desc FROM %s;" % self.error_type
        self.db.execute(select_sql)
        type_info = {}
        for item in self.db.fetchall():
            type_id_s = fill_zero(item[0], 2)
            type_info[type_id_s] = {"title": item[1], "desc": item[2]}
        return True, type_info


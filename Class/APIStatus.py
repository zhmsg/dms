#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Class import table_manager, TIME_FORMAT
from Check import check_sql_character, check_int, fill_zero
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

    def insert_service_module(self, service_title, service_desc):
        select_sql = "SELECT MAX(service_id) FROM %s;" % self.service_module
        result = self.db.execute(select_sql)
        if result == 0:
            service_id = 0
        else:
            service_id = self.db.fetchone()[0]
        insert_sql = "INSERT INTO %s (service_id,serivce_title,service_desc) VALUES(%s,'%s','%s');" \
                     % (self.service_module, service_id, service_title, service_desc)
        self.db.execute(insert_sql)
        return True, service_id

    def insert_function_module(self, service_id, function_title, function_desc):
        select_sql = "SELECT MAX(function_id) FROM %s WHERE service_id=%s;" % (self.function_module, service_id)
        result = self.db.execute(select_sql)
        if result == 0:
            function_id = 0
        else:
            function_id = self.db.fetchone()[0]
        insert_sql = "INSERT INTO %s (function_id,function_title,function_desc) VALUES(%s,'%s','%s');" \
                     % (self.function_module, function_id, function_title, function_desc)
        self.db.execute(insert_sql)
        return True, function_id

    def _insert_status_code(self, status_code, code_desc, adder):
        code_desc = check_sql_character(code_desc)
        add_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT IGNORE INTO %s (status_code,code_desc,add_time,adder) " \
                     "VALUES (%s,'%s','%s','%s');" % (self.status_code, status_code, code_desc, add_time, adder)
        result = self.db.execute(insert_sql)
        return result

    def new_status_code(self, service_id, fun_id, type_id, error_id, error_desc, adder):
        if check_int(service_id) is False:
            return False, "Bad service_id"
        if check_int(fun_id) is False:
            return False, "Bad fun_id"
        if check_int(type_id) is False:
            return False, "Bad type_id"
        if check_int(error_id) is False:
            return False, "Bad error_id"
        status_code = fill_zero(service_id, 2) + fill_zero(fun_id, 2) + fill_zero(type_id, 2) + fill_zero(error_id, 2)
        self._insert_status_code(status_code, error_desc, adder)
        return True, status_code

    def new_mul_status_code(self, service_id, fun_id, error_info, adder):
        if check_int(service_id) is False:
            return "Bad service_id"
        if check_int(fun_id) is False:
            return "Bad fun_id"
        basic_code = service_id * 1000000 + fun_id * 10000
        success_new = []
        for item in error_info:
            if "type_id" not in item:
                continue
            if "error_desc" not in item:
                continue
            type_id = item["type_id"]
            error_desc = item["error_desc"]
            if check_int(type_id) is False:
                continue
            error_code = basic_code + type_id * 100
            # 查询该模块下此类错误最大的状态码
            select_sql = "SELECT status_code FROM %s WHERE status_code>=%s AND status_code<%s " \
                         "ORDER BY status_code DESC LIMIT 1;" % (self.status_code, error_code, error_code + 100)
            result = self.db.execute(select_sql)
            if result > 0:
                error_code = self.db.fetchone()[0] + 1
            result = self._insert_status_code(error_code, error_desc, adder)
            if result == 1:
                success_new.append({"status_code": error_code, "error_desc": error_desc})
        return True, success_new

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

    def del_status_code(self, status_code):
        if type(status_code) != int:
            return False, "Bad status_code"
        delete_sql = "DELETE FROM %s WHERE status_code=%s;" % (self.status_code, status_code)
        self.db.execute(delete_sql)
        return True, "success"

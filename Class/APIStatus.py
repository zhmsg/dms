#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Class import TIME_FORMAT
from Check import check_sql_character, check_int, fill_zero, check_chinese_en, check_special_character

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class StatusManager:

    def __init__(self):
        self.db = DB()
        self.service_module = "service_module"
        self.function_module = "function_module"
        self.error_type = "error_type"
        self.status_code = "status_code"
        self.user = "sys_user"

    def insert_service_module(self, service_title, service_desc):
        if check_chinese_en(service_title) is False:
            return False, "Bad service_title"
        if check_special_character(service_desc) is False:
            return False, "Bad service_desc"
        select_sql = "SELECT MAX(service_id) FROM %s;" % self.service_module
        result = self.db.execute(select_sql)
        if result == 0:
            service_id = 0
        else:
            db_result = self.db.fetchone()[0]
            if db_result is None:
                service_id = 0
            else:
                service_id = db_result + 1
        insert_sql = "INSERT INTO %s (service_id,service_title,service_desc) VALUES (%s,'%s','%s');" \
                     % (self.service_module, service_id, service_title, service_desc)
        self.db.execute(insert_sql)
        return True, {"service_id": fill_zero(service_id, 2), "service_title": service_title, "service_desc": service_desc}

    def insert_function_module(self, service_id, function_title, function_desc):
        if check_chinese_en(function_title) is False:
            return False, "Bad function_title"
        if check_special_character(function_desc) is False:
            return False, "Bad function_desc"
        select_sql = "SELECT MAX(function_id) FROM %s WHERE service_id=%s;" % (self.function_module, service_id)
        result = self.db.execute(select_sql, auto_close=False)
        if result == 0:
            function_id = 0
        else:
            db_result = self.db.fetchone()[0]
            if db_result is None:
                function_id = 0
            else:
                function_id = db_result + 1
        insert_sql = "INSERT INTO %s (service_id,function_id,function_title,function_desc) VALUES (%s,%s,'%s','%s');" \
                     % (self.function_module, service_id, function_id, function_title, function_desc)
        self.db.execute(insert_sql)
        return True, {"function_id": fill_zero(function_id, 2), "function_title": function_title, "function_desc": function_desc}

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
            return False, "Bad service_id"
        if check_int(fun_id) is False:
            return False, "Bad fun_id"
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
            error_code = basic_code + type_id * 100 + 1
            # 查询该模块下此类错误最大的状态码
            select_sql = "SELECT status_code FROM %s WHERE status_code>=%s AND status_code<%s " \
                         "ORDER BY status_code DESC LIMIT 1;" % (self.status_code, error_code, error_code + 99)
            result = self.db.execute(select_sql)
            if result > 0:
                error_code = self.db.fetchone()[0] + 1
            result = self._insert_status_code(error_code, error_desc, adder)
            if result == 1:
                success_new.append({"status_code": fill_zero(error_code, 8), "error_desc": error_desc})
        return True, success_new

    def get_status_code(self, status_code=None):
        cols = ["status_code", "code_desc", "add_time", "adder"]
        if status_code is not None:
            where_value = dict(status_code=status_code)
        else:
            where_value = None
        items = self.db.execute_select(self.status_code, where_value=where_value, cols=cols)
        for item in items:
            item["status_code"] = fill_zero(item["status_code"], 8)
        return True, items

    def get_function_info(self):
        cols = ["service_id", "service_title", "service_desc"]
        items = self.db.execute_select(self.service_module, cols=cols)
        module_info = {}
        for item in items:
            service_id_s = fill_zero(item["service_id"], 2)
            module_info[service_id_s] = {"title": item["service_title"], "desc": item["service_desc"], "fun_info": {}}
        cols = ["service_id", "function_id", "function_title", "function_desc"]
        items = self.db.execute_select(self.function_module, cols=cols)
        for item in items:
            service_id_s = fill_zero(item["service_id"], 2)
            if service_id_s in module_info:
                fun_id_s = fill_zero(item["function_id"], 2)
                module_info[service_id_s]["fun_info"][fun_id_s] = {"title": item["function_title"],
                                                                   "desc": item["function_desc"]}
        return True, module_info

    def get_error_type(self):
        cols = ["type_id", "type_title", "type_desc"]
        items = self.db.execute_select(self.error_type, cols=cols)
        type_info = dict()
        for item in items:
            type_id_s = fill_zero(item["type_id"], 2)
            type_info[type_id_s] = item
        return True, type_info

    def del_status_code(self, status_code):
        if type(status_code) != int:
            return False, "Bad status_code"
        delete_sql = "DELETE FROM %s WHERE status_code=%s;" % (self.status_code, status_code)
        self.db.execute(delete_sql)
        return True, "success"

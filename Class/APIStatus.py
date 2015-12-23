#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Class import table_manager, TIME_FORMAT
from Check import check_chinese_en, check_http_method, check_path, check_sql_character, check_char_num_underline, check_char
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

    def new_status_code(self, fun_id, type_id, error_id, error_desc):
        if type(fun_id) != int or type(type_id) != int or type(error_id) != int:
            return False, "Bad fun_id or type_id or error_id"
        insert_sql = "INSERT IGNORE INTO %s (function_id,type_id,error_id,error_desc) VALUES (%d,%d,%d,'%s');" \
                     % (fun_id, type_id, error_id, error_desc)
        self.db.execute(insert_sql)
        return True, "success"

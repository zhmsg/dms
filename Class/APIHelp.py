#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from Tools.Mysql_db import DB
from Class import table_manager
from Check import check_chinese_en, check_http_method, check_path, check_sql_character

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class HelpManager:

    def __init__(self):
        self.db = DB()
        self.api_module = table_manager.api_module
        self.api_info = table_manager.api_info
        self.api_input = table_manager.api_input
        self.api_output = table_manager.api_output
        self.api_header = table_manager.api_header
        self.api_body = table_manager.api_body

    def new_api(self, module_no, api_title, api_path, api_method, api_desc):
        if check_chinese_en(api_title) is False:
            return False, "Bad api_title"
        if check_path(api_path) is False:
            return False, "Bad api_path"
        if check_http_method(api_method) is False:
            return False, "Bad api_method"
        api_desc = check_sql_character(api_desc)
        api_no = uuid.uuid1().hex
        # 新建 api_info
        insert_sql = "INSERT INTO %s (api_no,module_no,api_title,api_path,api_method,api_desc) " \
                     "VALUES('%s',%s,'%s','%s','%s','%s')" \
                     % (self.api_info, api_no, module_no, api_title, api_path, api_method, api_desc)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no", api_no}

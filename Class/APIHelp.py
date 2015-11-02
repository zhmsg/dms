#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
sys.path.append("..")
from Tools.Mysql_db import DB
from Class import table_manager

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
        # 新建 api_info
        insert_sql = "INSERT INTO %s (module_no,api_title,api_path,api_method,api_desc) VALUES(%s,'%s','%s','%s','%s')" \
                     % (self.api_info, module_no, api_title, api_path, api_method, api_desc)

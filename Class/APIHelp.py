#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from Tools.Mysql_db import DB
from Class import table_manager
from Check import check_chinese_en, check_http_method, check_path, check_sql_character, check_char_num_underline, check_char

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

    def new_api_info(self, module_no, api_title, api_path, api_method, api_desc):
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

    def new_api_header(self, api_no, header_params):
        if len(api_no) != 32:
            return False, "Bad api_no"
        value_sql = "VALUES "
        for key, value in header_params.items():
            if check_char_num_underline(key) is False:
                return False, "Bad header param %s" % key
            if "necessary" not in value or "desc" not in value:
                return False, "Bad header param %s, need necessary and desc" % key
            if value["necessary"] != 0 and value["necessary"] != 1:
                return False, "Bad header param %s, necessary must be 0 or 1" % key
            param_desc = check_sql_character(value["desc"])[:1000]
            value_sql += "('%s','%s',%s,'%s')" % (api_no, key, value["necessary"], param_desc)
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (api_no,param,necessary,param_desc) %s" % (self.api_header, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no", api_no}

    def new_api_body(self, api_no, body_params):
        if len(api_no) != 32:
            return False, "Bad api_no"
        value_sql = "VALUES "
        for key, value in body_params.items():
            if check_char_num_underline(key) is False:
                return False, "Bad body param %s" % key
            if "necessary" not in value or "desc" not in value or "type" not in value:
                return False, "Bad body param %s, need necessary type desc" % key
            if value["necessary"] != 0 and value["necessary"] != 1:
                return False, "Bad body param %s, necessary must be 0 or 1" % key
            if check_char(value["type"], 1, 20) is False:
                return False, "Bad body param %s, type must a-z" % key
            param_desc = check_sql_character(value["desc"])[:1000]
            value_sql += "('%s','%s',%s,'%s','%s')" % (api_no, key, value["necessary"], value["type"], param_desc)
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (api_no,param,necessary,type,param_desc) %s" % (self.api_body, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no", api_no}

    def new_api_input(self, api_no, input_examples):
        if len(api_no) != 32:
            return False, "Bad api_no"
        value_sql = "VALUES "
        for item in input_examples:
            if "desc" not in item or "example" not in item:
                return False, "input example need desc and example"
            input_desc = check_sql_character(item["desc"])[:150]
            input_example = check_sql_character(item["example"])
            value_sql += "('%s','%s','%s')" % (api_no, input_desc, input_example)
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (api_no,input_desc,input_example) %s" % (self.api_input, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no", api_no}

    def new_api_input(self, api_no, output_examples):
        if len(api_no) != 32:
            return False, "Bad api_no"
        value_sql = "VALUES "
        for item in output_examples:
            if "desc" not in item or "example" not in item:
                return False, "output example need desc and example"
            output_desc = check_sql_character(item["desc"])[:150]
            output_example = check_sql_character(item["example"])
            value_sql += "('%s','%s','%s')" % (api_no, output_desc, output_example)
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (api_no,input_desc,input_example) %s" % (self.api_output, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no", api_no}

    def get_module_list(self):
        select_sql = "SELECT module_no,module_name,module_prefix,module_desc FROM %s;" % self.api_module
        self.db.execute(select_sql)
        module_info = []
        for item in self.db.fetchall():
            module_info.append({"module_no": item[0], "module_name": item[1], "module_prefix": item[2], "module_desc": item[3]})
        return True, module_info
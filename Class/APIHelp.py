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
        if type(module_no) != int:
            return False , "Bad module_no"
        if check_chinese_en(api_title) is False:
            return False, "Bad api_title"
        if check_path(api_path) is False:
            return False, "Bad api_path"
        if check_http_method(api_method) is False:
            return False, "Bad api_method"

        api_desc = check_sql_character(api_desc)
        if len(api_desc) < 1:
            return False, "Bad api_desc"
        api_no = uuid.uuid1().hex
        # 新建 api_info
        add_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (api_no,module_no,api_title,api_path,api_method,api_desc,add_time) " \
                     "VALUES('%s',%s,'%s','%s','%s','%s','%s')" \
                     % (self.api_info, api_no, module_no, api_title, api_path, api_method, api_desc, add_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no": api_no}

    def new_api_header(self, api_no, header_params):
        if len(api_no) != 32:
            return False, "Bad api_no"
        value_sql = "VALUES "
        new_result = []
        for key, value in header_params.items():
            if check_char_num_underline(key) is False:
                return False, "Bad header param %s" % key
            if "necessary" not in value or "desc" not in value:
                return False, "Bad header param %s, need necessary and desc" % key
            if value["necessary"] != 0 and value["necessary"] != 1:
                return False, "Bad header param %s, necessary must be 0 or 1" % key
            param_desc = check_sql_character(value["desc"])[:1000]
            header_no = uuid.uuid1().hex
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s','%s','%s',%s,'%s','%s')" \
                         % (header_no, api_no, key, value["necessary"], param_desc, add_time)
            necessary = True if value["necessary"] == 1 else False
            new_result.append({"api_no": api_no, "header_no": header_no, "necessary": necessary, "param": key,
                               "desc": param_desc, "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (header_no,api_no,param,necessary,param_desc, add_time) %s" \
                     % (self.api_header, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, new_result

    def new_api_body(self, api_no, body_params):
        if len(api_no) != 32:
            return False, "Bad api_no"
        new_result = []
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
            body_no = uuid.uuid1().hex
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s', '%s','%s',%s,'%s','%s','%s')" \
                         % (body_no, api_no, key, value["necessary"], value["type"], param_desc, add_time)
            necessary = True if value["necessary"] == 1 else False
            new_result.append({"api_no": api_no, "body_no": body_no, "necessary": necessary, "param": key,
                               "desc": param_desc, "type": value["type"], "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (body_no,api_no,param,necessary,type,param_desc, add_time) %s" \
                     % (self.api_body, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, new_result

    def new_api_input(self, api_no, input_examples):
        if len(api_no) != 32:
            return False, "Bad api_no"
        new_result = []
        value_sql = "VALUES "
        for item in input_examples:
            if "desc" not in item or "example" not in item:
                return False, "input example need desc and example"
            input_desc = check_sql_character(item["desc"])[:150]
            input_example = check_sql_character(item["example"])
            if len(input_desc) < 1:
                return False, "Bad input_desc"
            if len(input_example) < 1:
                return False, "Bad input_example"
            input_no = uuid.uuid1().hex
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s','%s','%s','%s','%s')" % (input_no,api_no, input_desc, input_example, add_time)
            new_result.append({"api_no": api_no, "input_no": input_no, "desc": input_desc,
                               "example": input_example, "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (input_no,api_no,input_desc,input_example,add_time) %s" % (self.api_input, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, new_result

    def new_api_output(self, api_no, output_examples):
        if len(api_no) != 32:
            return False, "Bad api_no"
        new_result = []
        value_sql = "VALUES "
        for item in output_examples:
            if "desc" not in item or "example" not in item:
                return False, "output example need desc and example"
            output_desc = check_sql_character(item["desc"])[:150]
            output_example = check_sql_character(item["example"])
            if len(output_desc) < 1:
                return False, "Bad output_desc"
            if len(output_example) < 1:
                return False, "Bad output_example"
            output_no = uuid.uuid1().hex
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s','%s','%s','%s','%s')" % (output_no,api_no, output_desc, output_example, add_time)
            new_result.append({"api_no": api_no, "input_no": output_no, "desc": output_desc,
                               "example": output_example, "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (output_no,api_no,output_desc,output_example,add_time) %s" \
                     % (self.api_output, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, new_result

    def get_module_list(self, module_no=None):
        select_sql = "SELECT module_no,module_name,module_prefix,module_desc FROM %s" % self.api_module
        if module_no is not None and type(module_no) == int:
            select_sql += " WHERE module_no=%s" % module_no
        select_sql += ";"
        self.db.execute(select_sql)
        module_info = []
        for item in self.db.fetchall():
            module_info.append({"module_no": item[0], "module_name": item[1], "module_prefix": item[2], "module_desc": item[3]})
        return True, module_info

    def get_api_info(self, api_no):
        if len(api_no) != 32:
            return False, "Bad api_no"
        # get basic info
        basic_info_col = ("module_no", "api_no", "api_title", "api_path", "api_method", "api_desc", "module_name",
                          "module_prefix", "module_desc")
        select_sql = "SELECT m.%s FROM %s AS i, api_module AS m WHERE i.module_no=m.module_no AND api_no='%s';" \
                     % (",".join(basic_info_col), self.api_info, api_no)
        result = self.db.execute(select_sql)
        if result <= 0:
            return False, "Not Exist api_no"
        db_info = self.db.fetchone()
        basic_info = {}
        for i in range(len(db_info)):
            basic_info[basic_info_col[i]] = db_info[i]
        basic_info["api_url"] = basic_info["module_prefix"].rstrip("/") + "/" + basic_info["api_path"].lstrip("/")
        # 获得请求头部参数列表
        select_sql = "SELECT header_no,api_no,param,necessary,param_desc FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_header, api_no)
        self.db.execute(select_sql)
        header_info = []
        for item in self.db.fetchall():
            necessary = True if item[3] == "" else False
            header_info.append({"header_no": item[0], "api_no": item[1], "param": item[2], "necessary": necessary,
                                "param_desc": item[4]})
        # 获得请求主体参数列表
        select_sql = "SELECT body_no,api_no,param,necessary,type,param_desc FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_body, api_no)
        self.db.execute(select_sql)
        body_info = []
        for item in self.db.fetchall():
            necessary = True if item[3] == "" else False
            body_info.append({"body_no": item[0], "api_no": item[1], "param": item[2], "necessary": necessary,
                              "type": item[4], "param_desc": item[5]})
        # 获得请求示例
        select_sql = "SELECT input_no,api_no,input_desc,input_example FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_input, api_no)
        self.db.execute(select_sql)
        input_info = []
        for item in self.db.fetchall():
            input_info.append({"input_no": item[0], "api_no": item[1], "input_desc": item[2], "input_example": item[3]})
        # 获得返回示例
        select_sql = "SELECT output_no,api_no,output_desc,output_example FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_output, api_no)
        self.db.execute(select_sql)
        output_info = []
        for item in self.db.fetchall():
            output_info.append({"output_no": item[0], "api_no": item[1], "output_desc": item[2], "output_example": item[3]})
        return True, {"basic_info": basic_info, "header_info": header_info, "body_info": body_info,
                      "input_info": input_info, "output_info": output_info}

    def get_api_list(self, module_no):
        if type(module_no) != int:
            return False, "Bad module_no"
        select_sql = "SELECT api_no,module_no,api_title,api_path,api_method,api_desc FROM %s WHERE module_no=%s;" \
                     % (self.api_info, module_no)
        self.db.execute(select_sql)
        api_list = []
        for item in self.db.fetchall():
            api_list.append({"api_no": item[0], "module_no": item[1], "api_title": item[2], "api_path": item[3],
                             "api_method": item[4], "api_desc": item[5]})
        return True, api_list

    def del_api_header(self, header_no):
        delete_sql = "DELETE FROM %s WHERE " % self.api_header

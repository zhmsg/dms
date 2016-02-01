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


class HelpManager:

    def __init__(self):
        self.db = DB()
        self.api_module = table_manager.api_module
        self.api_info = table_manager.api_info
        self.api_input = table_manager.api_input
        self.api_output = table_manager.api_output
        self.api_header = table_manager.api_header
        self.predefine_header = table_manager.predefine_header
        self.api_body = table_manager.api_body
        self.predefine_param = table_manager.predefine_param
        self.api_care = table_manager.api_care
        self.user = "sys_user"

    def new_api_info(self, module_no, api_title, api_path, api_method, api_desc):
        if type(module_no) != int:
            return False , "Bad module_no"
        if check_path(api_path) is False:
            return False, "Bad api_path"
        if check_http_method(api_method) is False:
            return False, "Bad api_method"
        api_title = check_sql_character(api_title)
        api_desc = check_sql_character(api_desc)
        if len(api_desc) < 1:
            return False, "Bad api_desc"
        api_no = uuid.uuid1().hex
        # 新建 api_info
        add_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (api_no,module_no,api_title,api_path,api_method,api_desc,add_time,update_time) " \
                     "VALUES('%s',%s,'%s','%s','%s','%s','%s','%s')" \
                     % (self.api_info, api_no, module_no, api_title, api_path, api_method, api_desc, add_time, add_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"api_no": api_no}

    def set_api_update(self, api_no):
        update_time = datetime.now().strftime(TIME_FORMAT)
        update_sql = "UPDATE %s SET update_time='%s' WHERE api_no='%s';" % (self.api_info, update_time, api_no)
        self.db.execute(update_sql)
        return True

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
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s','%s',%s,'%s','%s')" \
                         % (api_no, key, value["necessary"], param_desc, add_time)
            necessary = True if value["necessary"] == 1 else False
            new_result.append({"api_no": api_no, "necessary": necessary, "param": key,
                               "desc": param_desc, "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (api_no,param,necessary,param_desc, add_time) %s " \
                     "ON DUPLICATE KEY UPDATE necessary=VALUES(necessary),param_desc=VALUES(param_desc),add_time=VALUES(add_time)" \
                     % (self.api_header, value_sql)
        result = self.db.execute(insert_sql)
        if result < 1:
            return False, "sql execute result is %s " % result
        self.set_api_update(api_no)
        return True, new_result

    def new_predefine_header(self, api_no, param):
        if len(api_no) != 32:
            return False, "Bad api_no"
        add_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (api_no,param,param_type,add_time) VALUES ('%s','%s','header','%s') " \
                     "ON DUPLICATE KEY UPDATE add_time=VALUES(add_time);" \
                     % (self.predefine_param, api_no, param, add_time)
        self.db.execute(insert_sql)
        return True

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
        self.set_api_update(api_no)
        return True, new_result

    def new_api_input(self, api_no, input_examples):
        if len(api_no) != 32:
            return False, "Bad api_no"
        new_result = []
        value_sql = "VALUES "
        for item in input_examples:
            if "desc" not in item or "example" not in item:
                return False, "input example need desc and example"
            input_desc = check_sql_character(item["desc"])[:550]
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
        self.set_api_update(api_no)
        return True, new_result

    def new_api_output(self, api_no, output_examples):
        if len(api_no) != 32:
            return False, "Bad api_no"
        new_result = []
        value_sql = "VALUES "
        for item in output_examples:
            if "desc" not in item or "example" not in item:
                return False, "output example need desc and example"
            output_desc = check_sql_character(item["desc"])[:550]
            output_example = check_sql_character(item["example"])
            if len(output_desc) < 1:
                return False, "Bad output_desc"
            if len(output_example) < 1:
                return False, "Bad output_example"
            output_no = uuid.uuid1().hex
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s','%s','%s','%s','%s')" % (output_no,api_no, output_desc, output_example, add_time)
            new_result.append({"api_no": api_no, "output_no": output_no, "desc": output_desc,
                               "example": output_example, "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (output_no,api_no,output_desc,output_example,add_time) %s" \
                     % (self.api_output, value_sql)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        self.set_api_update(api_no)
        return True, new_result

    def new_api_care(self, api_no, user_name, care_level=2):
        if len(api_no) != 32:
            return False, "Bad api_no"
        care_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (api_no,user_name,care_time,level) VALUES('%s','%s','%s',%s)" \
                     " ON DUPLICATE KEY UPDATE care_time=VALUES(care_time);" \
                     % (self.api_care, api_no, user_name, care_time, care_level)
        result = self.db.execute(insert_sql)
        if result < 1:
            return False, "sql execute result is %s " % result
        return True, {"user_name": user_name, "api_no": api_no, "care_time": care_time}

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
        basic_info_col = ("module_no", "api_no", "api_title", "api_path", "api_method", "api_desc", "add_time",
                          "update_time", "module_name", "module_prefix", "module_desc")
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
        basic_info["add_time"] = basic_info["add_time"].strftime(TIME_FORMAT) if basic_info["add_time"] is not None else ""
        basic_info["update_time"] = basic_info["update_time"].strftime(TIME_FORMAT) if basic_info["update_time"] is not None else ""
        # 获得请求头部参数列表
        select_sql = "SELECT api_no,param,necessary,param_desc FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_header, api_no)
        self.db.execute(select_sql)
        header_info = []
        for item in self.db.fetchall():
            necessary = True if item[2] == "" else False
            header_info.append({"api_no": item[0], "param": item[1], "necessary": necessary,
                                "param_desc": item[3]})
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
        # 获得关注列表
        select_sql = "SELECT api_no,c.user_name,care_time,nick_name,level FROM sys_user as su,%s as c " \
                     "WHERE su.user_name=c.user_name AND api_no='%s';" % (self.api_care, api_no)
        self.db.execute(select_sql)
        care_info = []
        for item in self.db.fetchall():
            care_info.append({"api_no": item[0], "user_name": item[1], "care_time": item[2].strftime(TIME_FORMAT),
                              "nick_name": item[3], "level": item[4]})
        return True, {"basic_info": basic_info, "header_info": header_info, "body_info": body_info,
                      "input_info": input_info, "output_info": output_info, "care_info": care_info}

    def get_api_list(self, module_no):
        if type(module_no) != int:
            return False, "Bad module_no"
        select_sql = "SELECT api_no,module_no,api_title,api_path,api_method,api_desc FROM %s WHERE module_no=%s ORDER BY add_time;" \
                     % (self.api_info, module_no)
        self.db.execute(select_sql)
        api_list = []
        for item in self.db.fetchall():
            api_list.append({"api_no": item[0], "module_no": item[1], "api_title": item[2], "api_path": item[3],
                             "api_method": item[4], "api_desc": item[5]})
        return True, api_list

    def del_api_header(self, api_no, param):
        if len(api_no) != 32:
            return False, "Bad api_no"
        delete_sql = "DELETE FROM %s WHERE api_no='%s' AND param='%s';" % (self.api_header, api_no, param)
        result = self.db.execute(delete_sql)
        self.set_api_update(api_no)
        return True, result

    def del_api_body(self, body_no):
        if len(body_no) != 32:
            return False, "Bad body_no"
        delete_sql = "DELETE FROM %s WHERE body_no='%s';" % (self.api_body, body_no)
        result = self.db.execute(delete_sql)
        return True, result

    def del_api_input(self, input_no):
        if len(input_no) != 32:
            return False, "Bad input_no"
        delete_sql = "DELETE FROM %s WHERE input_no='%s';" % (self.api_input, input_no)
        result = self.db.execute(delete_sql)
        return True, result

    def del_api_output(self, output_no):
        if len(output_no) != 32:
            return False, "Bad output_no"
        delete_sql = "DELETE FROM %s WHERE output_no='%s';" % (self.api_output, output_no)
        result = self.db.execute(delete_sql)
        return True, result

    def del_api_care(self, api_no, user_name):
        if len(api_no) != 32:
            return False, "Bad api_no"
        delete_sql = "DELETE FROM %s WHERE api_no='%s' AND user_name='%s';" % (self.api_care, api_no, user_name)
        result = self.db.execute(delete_sql)
        return True, result

    def del_api_info(self, api_no, user_name):
        if len(api_no) != 32:
            return False, "Bad api_no"
        select_sql = "SELECT level FROM %s WHERE api_no='%s' AND user_name='%s' AND level=0;" \
                     % (self.api_care, api_no, user_name)
        result = self.db.execute(select_sql)
        if result <= 0:
            return False, "user can not delete this api"
        delete_sql = "DELETE FROM %s WHERE api_no='%s';" % (self.api_info, api_no)
        update_sql = "UPDATE %s SET level=3 WHERE api_no='%s' AND user_name='%s';" \
                     % (self.api_care, api_no, user_name)
        result = self.db.execute(delete_sql)
        self.db.execute(update_sql)
        self.del_api_other_info(api_no)
        return True, result

    def del_api_other_info(self, api_no):
        delete_sql_format = "DELETE FROM %s WHERE api_no='" + api_no + "';"
        for t in (self.api_header, self.api_input, self.api_body, self.api_output):
            delete_sql = delete_sql_format % t
            self.db.execute(delete_sql)
        return True, "success"

    def notice_change(self, api_no, change_message):
        # 获得所有关注的人
        select_sql = "SELECT c.user_name,wx_id,nick_name FROM %s as su,%s as c " \
                     "WHERE su.user_name=c.user_name AND api_no='%s' AND wx_id is not null;" \
                     % (self.user, self.api_care, api_no)
        self.db.execute(select_sql)
        care_info = []
        for item in self.db.fetchall():
            care_info.append({"user_name": item[0], "wx_id": item[1], "nick_name": item[2]})
        # 获取API基本信息
        basic_info_col = ("api_no", "api_title", "api_path", "api_method", "api_desc")
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
        # 逐个发送微信消息
        for care_user in care_info:
            look_url = "dms.gene.ac/dev/api/info/?api_no=%s" % api_no
            wx.send_api_change_template(basic_info["api_url"], basic_info["api_title", look_url, care_user["wx_id"]], change_message)
        return True, "success"

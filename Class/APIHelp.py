#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
from time import time
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Class import TIME_FORMAT
from Check import check_chinese_en, check_http_method, check_path, check_sql_character, check_char_num_underline, check_char, check_int

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class HelpManager:

    def __init__(self):
        self.db = DB()
        self.api_module = "api_module"
        self.api_info = "api_info"
        self.api_input = "api_input"
        self.api_output = "api_output"
        self.api_header = "api_header"
        self.predefine_header = "predefine_header"
        self.predefine_body = "predefine_body"
        self.api_body = "api_body"
        self.predefine_param = "predefine_param"
        self.api_care = "api_care"
        self.module_care = "module_care"
        self.send_message = "send_message"
        self.test_env = "test_env"
        self.api_status_desc = [u"新建", u"修改中", u"已完成", u"待废弃", u"已废弃", u"已删除"]
        self.user = "sys_user"

    def new_api_module(self, module_name, module_prefix, module_desc, module_part, module_env):
        if check_chinese_en(module_name, 1, 35) is False:
            return False, "Bad module_name."
        if check_path(module_prefix, 1, 35) is False:
            return False, "Bad module_prefix"
        if check_int(module_part, max_v=9999) is False:
            return False, "Bad module_part"
        if type(module_env) != list:
            return False, "Bad module_env"
        if len(module_env) not in range(1, 6):
            print(module_env)
            return False, "Bad module_env."
        module_desc = check_sql_character(module_desc)[:240]
        module_env_s = ""
        for env_no in module_env:
            if type(env_no) != int:
                return False, "Bad env_no"
            module_env_s += "%s|" % env_no
        insert_sql = "INSERT INTO %s (module_name,module_prefix,module_desc,module_part,module_env) " \
                     "VALUES ('%s','%s','%s',%s,'%s');" \
                     % (self.api_module, module_name, module_prefix, module_desc, module_part, module_env_s[:-1])
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, "success"

    def update_api_module(self, module_no, module_name, module_prefix, module_desc, module_part, module_env):
        if check_chinese_en(module_name, 0, 35) is False:
            return False, "Bad module_name."
        if check_path(module_prefix, 0, 35) is False:
            return False, "Bad module_prefix"
        if check_int(module_part, max_v=9999) is False:
            return False, "Bad module_part"
        if type(module_env) != list:
            return False, "Bad module_env"
        if len(module_env) not in range(1, 6):
            print(module_env)
            return False, "Bad module_env."
        module_desc = check_sql_character(module_desc)[:240]
        module_env_s = ""
        for env_no in module_env:
            if type(env_no) != int:
                return False, "Bad env_no"
            module_env_s += "%s|" % env_no
        update_sql = "UPDATE %s SET module_name='%s',module_prefix='%s',module_desc='%s',module_part=%s,module_env='%s' " \
                     "WHERE module_no=%s;"  \
                     % (self.api_module, module_name, module_prefix, module_desc, module_part, module_env_s[:-1], module_no)
        result = self.db.execute(update_sql)
        return True, "success"

    def del_api_module(self, module_no):
        delete_sql = "DELETE FROM %s WHERE module_no=%s;" % (self.api_module, module_no)
        self.db.execute(delete_sql)
        return True, "success"

    def new_api_info(self, module_no, api_title, api_path, api_method, api_desc):
        if type(module_no) != int:
            return False , "Bad module_no"
        if check_path(api_path) is False:
            return False, "Bad api_path"
        if api_path.endswith("/") is False:
            return False, u"api path should end with /"
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

    def update_api_info(self, api_no, module_no, api_title, api_path, api_method, api_desc):
        if len(api_no) != 32:
            return False, "Bad api_no"
        if type(module_no) != int:
            return False , "Bad module_no"
        if check_path(api_path) is False:
            return False, "Bad api_path"
        if api_path.endswith("/") is False:
            return False, u"api path should end with /"
        if check_http_method(api_method) is False:
            return False, "Bad api_method"
        api_title = check_sql_character(api_title)
        api_desc = check_sql_character(api_desc)
        if len(api_desc) < 1:
            return False, "Bad api_desc"
        # 更新 api_info
        update_time = datetime.now().strftime(TIME_FORMAT)
        update_sql = "UPDATE %s SET module_no=%s,api_title='%s',api_path='%s',api_method='%s',api_desc='%s',update_time='%s' " \
                     "WHERE api_no='%s'; "  \
                     % (self.api_info, module_no, api_title, api_path, api_method, api_desc, update_time, api_no)
        result = self.db.execute(update_sql)
        return True, "success"

    def set_api_update(self, api_no):
        update_time = datetime.now().strftime(TIME_FORMAT)
        update_sql = "UPDATE %s SET update_time='%s' WHERE api_no='%s';" % (self.api_info, update_time, api_no)
        self.db.execute(update_sql)
        return True

    def set_api_status(self, api_no, status):
        if len(api_no) != 32:
            return False, "Bad api_no"
        update_time = datetime.now().strftime(TIME_FORMAT)
        update_sql = "UPDATE %s SET update_time='%s',status=%s WHERE api_no='%s';" \
                     % (self.api_info, update_time, status, api_no)
        self.db.execute(update_sql)
        return True, "success"

    def new_test_env(self, env_name, env_address):
        insert_sql = "INSERT INTO %s VALUES ('%s','%s');" % (self.test_env, env_name, env_address)
        self.db.execute(insert_sql)
        return True, "success"

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
        self.set_api_update(api_no)
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
            add_time = datetime.now().strftime(TIME_FORMAT)
            value_sql += "('%s','%s',%s,'%s','%s','%s')" \
                         % (api_no, key, value["necessary"], value["type"], param_desc, add_time)
            necessary = True if value["necessary"] == 1 else False
            new_result.append({"api_no": api_no, "necessary": necessary, "param": key, "desc": param_desc,
                               "type": value["type"], "add_time": add_time})
        if len(value_sql) < 8:
            return True
        insert_sql = "INSERT INTO %s (api_no,param,necessary,type,param_desc,add_time) %s " \
                     "ON DUPLICATE KEY UPDATE necessary=VALUES(necessary),param_desc=VALUES(param_desc),type=VALUES(type)" \
                     % (self.api_body, value_sql)
        result = self.db.execute(insert_sql)
        self.set_api_update(api_no)
        return True, new_result

    def new_predefine_param(self, api_no, param, param_type, add_time=None):
        if len(api_no) != 32:
            return False, "Bad api_no"
        if param_type not in ("header", "body"):
            return False, "Bad param_type"
        if add_time is None:
            add_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (api_no,param,param_type,add_time) VALUES ('%s','%s','%s','%s') " \
                     "ON DUPLICATE KEY UPDATE add_time=VALUES(add_time);" \
                     % (self.predefine_param, api_no, param, param_type, add_time)
        self.db.execute(insert_sql)
        return True, "Success"

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

    def new_module_care(self, module_no, user_name, care_level=2):
        if type(module_no) != int:
            return False, "Bad module_no"
        care_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (module_no,user_name,care_time,level) VALUES('%s','%s','%s',%s)" \
                     " ON DUPLICATE KEY UPDATE care_time=VALUES(care_time);" \
                     % (self.module_care, module_no, user_name, care_time, care_level)
        result = self.db.execute(insert_sql)
        if result < 1:
            return False, "sql execute result is %s " % result
        return True, {"user_name": user_name, "module_no": module_no, "care_time": care_time}

    def new_send_message(self, send_user, rec_user, content):
        content = check_sql_character(content)
        rec_user_s = ",".join(rec_user)[:500]
        send_time = int(time())
        insert_sql = "INSERT INTO %s (send_user,rec_user,send_time,content) VALUES ('%s','%s',%s,'%s');" \
                     % (self.send_message, send_user, rec_user_s, send_time, content)
        self.db.execute(insert_sql)
        return True, "success"

    def get_test_env(self, env_no_list=None):
        if env_no_list is None:
            select_sql = "SELECT env_no,env_name,env_address FROM %s;" % self.test_env
        elif type(env_no_list) == list and len(env_no_list) >= 1 and len(env_no_list) <= 5:
            union_sql_list = []
            for env_no in env_no_list:
                if type(env_no) != int:
                    return False, "Bad env_no_list"
                part_select_sql = "SELECT env_no,env_name,env_address FROM %s WHERE env_no=%s" % (self.test_env, env_no)
                union_sql_list.append(part_select_sql)
            select_sql = " UNION ".join(union_sql_list)
        else:
            return False, "Bad env_no_list"
        self.db.execute(select_sql)
        db_result = self.db.fetchall()
        env_info = []
        for item in db_result:
            env_info.append({"env_no": item[0], "env_name": item[1], "env_address": item[2]})
        return True, env_info

    def get_module_list(self, module_no=None):
        select_sql = "SELECT module_no,module_name,module_prefix,module_desc,module_part,module_env FROM %s" % self.api_module
        if module_no is not None and type(module_no) == int:
            select_sql += " WHERE module_no=%s" % module_no
        select_sql += ";"
        self.db.execute(select_sql)
        module_info = {"api": [], "service": [], "jy": []}
        for item in self.db.fetchall():
            info = {"module_no": item[0], "module_name": item[1], "module_prefix": item[2], "module_desc": item[3],
                    "module_part": item[4], "module_env": item[5]}
            if item[4] == 1:
                module_info["api"].append(info)
            elif item[4] == 2:
                module_info["service"].append(info)
            elif item[4] == 3:
                module_info["jy"].append(info)
        return True, module_info

    def get_module_care_list(self, module_no):
        # 获得关注列表
        select_sql = "SELECT module_no,c.user_name,care_time,nick_name,level,email FROM sys_user as su,%s as c " \
                     "WHERE su.user_name=c.user_name AND module_no='%s';" % (self.module_care, module_no)
        self.db.execute(select_sql)
        care_info = []
        for item in self.db.fetchall():
            care_info.append({"module_no": item[0], "user_name": item[1], "care_time": item[2].strftime(TIME_FORMAT),
                              "nick_name": item[3], "level": item[4], "email": item[5]})
        return care_info

    def get_api_basic_info(self, api_no):
        # get basic info
        basic_info_col = ("module_no", "api_no", "api_title", "api_path", "api_method", "api_desc", "add_time",
                          "update_time", "module_name", "module_prefix", "module_desc", "module_env", "status")
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
        return True, basic_info

    def get_api_care_info(self, api_no):
        # 获得关注列表
        select_sql = "SELECT api_no,c.user_name,care_time,nick_name,level,email FROM sys_user as su,%s as c " \
                     "WHERE su.user_name=c.user_name AND api_no='%s';" % (self.api_care, api_no)
        self.db.execute(select_sql)
        care_info = []
        for item in self.db.fetchall():
            care_info.append({"api_no": item[0], "user_name": item[1], "care_time": item[2].strftime(TIME_FORMAT),
                              "nick_name": item[3], "level": item[4], "email": item[5]})
        return care_info

    def get_api_info(self, api_no):
        if len(api_no) != 32:
            return False, "Bad api_no"
        # get basic info
        result, basic_info = self.get_api_basic_info(api_no)
        if result is False:
            return False, basic_info
        # 获得请求头部参数列表
        select_sql = "SELECT api_no,param,necessary,param_desc FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_header, api_no)
        self.db.execute(select_sql)
        header_info = []
        for item in self.db.fetchall():
            necessary = True if item[2] == "\x01" else False
            header_info.append({"api_no": item[0], "param": item[1], "necessary": necessary,
                                "param_desc": item[3]})
        # 获得请求主体参数列表
        select_sql = "SELECT api_no,param,necessary,type,param_desc FROM %s WHERE api_no='%s' ORDER BY add_time;" \
                     % (self.api_body, api_no)
        self.db.execute(select_sql)
        body_info = []
        for item in self.db.fetchall():
            necessary = True if item[2] == "\x01" else False
            body_info.append({"api_no": item[0], "param": item[1], "necessary": necessary,
                              "type": item[3], "param_desc": item[4]})
        # 获得预定义参数列表
        select_sql = "SELECT param,param_type FROM %s WHERE api_no='%s' ORDER BY add_time;" % (self.predefine_param, api_no)
        self.db.execute(select_sql)
        predefine_param = {"header": [], "body": []}
        for item in self.db.fetchall():
            if item[1] in predefine_param:
                predefine_param[item[1]].append(item[0])
        # 获得预定义头部参数信息
        select_sql = "SELECT param,necessary,param_desc FROM %s;" % self.predefine_header
        self.db.execute(select_sql)
        predefine_header = {}
        for item in self.db.fetchall():
            necessary = True if item[1] == "\x01" else False
            predefine_header[item[0]] = {"param": item[0], "necessary": necessary, "param_desc": item[2]}
        # 获得预定义头部主体信息
        select_sql = "SELECT param,necessary,type,param_desc FROM %s;" % self.predefine_body
        self.db.execute(select_sql)
        predefine_body = {}
        for item in self.db.fetchall():
            necessary = True if item[1] == "\x01" else False
            predefine_body[item[0]] = {"param": item[0], "type": item[2], "necessary": necessary, "param_desc": item[3]}
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
        care_info = self.get_api_care_info(api_no)
        return True, {"basic_info": basic_info, "header_info": header_info, "body_info": body_info,
                      "input_info": input_info, "output_info": output_info, "care_info": care_info,
                      "predefine_param": predefine_param, "predefine_header": predefine_header,
                      "predefine_body": predefine_body}

    def get_api_list(self, module_no):
        if type(module_no) != int:
            return False, "Bad module_no"
        select_sql = "SELECT api_no,module_no,api_title,api_path,api_method,api_desc FROM %s WHERE module_no=%s ORDER BY api_path;" \
                     % (self.api_info, module_no)
        self.db.execute(select_sql)
        api_list = []
        for item in self.db.fetchall():
            api_list.append({"api_no": item[0], "module_no": item[1], "api_title": item[2], "api_path": item[3],
                             "api_method": item[4], "api_desc": item[5]})
        care_info = self.get_module_care_list(module_no)
        return True, {"api_list": api_list, "care_info": care_info}

    def del_api_header(self, api_no, param):
        if len(api_no) != 32:
            return False, "Bad api_no"
        delete_sql = "DELETE FROM %s WHERE api_no='%s' AND param='%s';" % (self.api_header, api_no, param)
        result = self.db.execute(delete_sql)
        self.set_api_update(api_no)
        return True, result

    def del_api_body(self, api_no, param):
        if len(api_no) != 32:
            return False, "Bad api_no"
        delete_sql = "DELETE FROM %s WHERE api_no='%s' AND param='%s';" % (self.api_body, api_no, param)
        result = self.db.execute(delete_sql)
        return True, result

    def del_predefine_param(self, api_no, param):
        if len(api_no) != 32:
            return False, "Bad api_no"
        delete_sql = "DELETE FROM %s WHERE api_no='%s' AND param='%s';" % (self.predefine_param, api_no, param)
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
        delete_sql = "DELETE FROM %s WHERE api_no='%s' AND user_name='%s' AND level <> 0;" % (self.api_care, api_no, user_name)
        result = self.db.execute(delete_sql)
        return True, result

    def del_module_care(self, module_no, user_name, level=2):
        if type(module_no) != int:
            return False, "Bad module_no"
        delete_sql = "DELETE FROM %s WHERE module_no='%s' AND user_name='%s' AND level=%s;" \
                     % (self.module_care, module_no, user_name, level)
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


if __name__ == "__main__":
    api_help = HelpManager()
    api_help.get_test_env([2, 3])

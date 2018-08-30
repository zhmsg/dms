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
from Check import check_chinese_en, check_http_method, check_path, check_sql_character, check_int

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class HelpManager:

    def __init__(self):
        self.db = DB()
        self.api_part_info = "api_part_info"
        self.api_module = "api_module"
        self.api_info = "api_info"
        self.t_example = "api_example"
        self.api_header = "api_header"
        self.predefine_header = "predefine_header"
        self.predefine_body = "predefine_body"
        self.api_body = "api_body"
        self.predefine_param = "predefine_param"
        self.api_care = "api_care"
        self.module_care = "module_care"
        self.send_message = "send_message"
        self.test_env = "test_env"
        self.api_stage_desc = [u"新建", u"修改中", u"已完成", u"待废弃", u"已废弃", u"已删除"]
        self.user = "sys_user"

    def new_api_module(self, module_name, module_prefix, module_desc, module_part, module_env):
        module_name = module_name.strip(" ")
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
        if len(module_env) not in range(1, 10):
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

    def set_api_stage(self, api_no, stage):
        if len(api_no) != 32:
            return False, "Bad api_no"
        if stage <= 0 or stage > 5:
            return False, "Bad stage"
        update_time = datetime.now().strftime(TIME_FORMAT)
        update_sql = "UPDATE %s SET update_time='%s',stage=%s WHERE api_no='%s';" \
                     % (self.api_info, update_time, stage, api_no)
        self.db.execute(update_sql)
        return True, "success"

    def new_test_env(self, env_name, env_address):
        insert_sql = "INSERT INTO %s VALUES ('%s','%s');" % (self.test_env, env_name, env_address)
        self.db.execute(insert_sql)
        return True, "success"

    def insert_api_header(self, api_no, param, necessary, param_desc, status=1):
        add_time = datetime.now().strftime(TIME_FORMAT)
        update_time = int(time())
        param_desc = param_desc[:1000]
        kwargs = dict(api_no=api_no, param=param, necessary=necessary, param_desc=param_desc, status=status,
                      add_time=add_time, update_time=update_time)
        l = self.db.execute_insert(self.api_header, kwargs, ignore=True)
        if l == 0:
            self.update_api_header(**kwargs)
        self.set_api_update(api_no)
        return True, kwargs

    def insert_api_body(self, api_no, param, necessary, param_type, param_desc, status=1):
        add_time = datetime.now().strftime(TIME_FORMAT)
        update_time = int(time())
        param_desc = param_desc[:1000]
        kwargs = dict(api_no=api_no, param=param, necessary=necessary, type=param_type, param_desc=param_desc,
                      status=status, add_time=add_time, update_time=update_time)
        l = self.db.execute_insert(self.api_body, kwargs, ignore=True)
        if l == 0:
            self.update_api_body(**kwargs)
        self.set_api_update(api_no)
        return True, kwargs

    def update_api_header(self, api_no, param, **kwargs):
        kwargs.pop("add_time")
        l = self.db.execute_update(self.api_header, update_value=kwargs, where_value=dict(api_no=api_no, param=param))
        return l

    def update_api_body(self, api_no, param, **kwargs):
        kwargs.pop("add_time")
        l = self.db.execute_update(self.api_body, update_value=kwargs, where_value=dict(api_no=api_no, param=param))
        return l

    def new_predefine_param(self, api_no, param, param_type, add_time=None):
        if len(api_no) != 32:
            return False, "Bad api_no"
        if param_type not in ("header", "body"):
            return False, "Bad param_type"
        if add_time is None:
            add_time = datetime.now().strftime(TIME_FORMAT)
        r_data = {"api_no": api_no, "param": param, "param_type": param_type, "add_time": add_time}
        result = self.db.execute_insert(self.predefine_param, r_data, ignore=True)
        self.set_api_update(api_no)
        r_data["result"] = result
        return True, r_data

    def insert_api_example(self, api_no, example_type, example_desc, example_content):
        example_no = uuid.uuid4().hex
        add_time = time()
        kwargs = dict(example_no=example_no, example_type=example_type, api_no=api_no, example_desc=example_desc,
                      example_content=example_content, add_time=add_time)
        l = self.db.execute_insert(self.t_example, kwargs)
        self.set_api_update(api_no)
        return True, kwargs

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
        elif type(env_no_list) == list and 1 <= len(env_no_list) <= 10:
            union_sql_list = []
            for env_no in env_no_list:
                if type(env_no) != int:
                    return False, "Bad env_no_list"
                part_select_sql = "SELECT env_no,env_name,env_address FROM %s WHERE env_no=%s" % (self.test_env, env_no)
                union_sql_list.append(part_select_sql)
            select_sql = " UNION ".join(union_sql_list)
        else:
            return False, "Bad env_no_list"
        self.db.execute(select_sql, auto_close=False)
        db_result = self.db.fetchall()
        env_info = []
        for item in db_result:
            env_info.append({"env_no": item[0], "env_name": item[1], "env_address": item[2]})
        return True, env_info

    def get_part_list(self, user_name):
        cols = ["part_no", "part_name", "part_desc", "part_detail"]
        part_list = self.db.execute_select(self.api_part_info, cols=cols)
        return part_list

    def get_part_api(self, user_name):
        part_list = self.get_part_list(user_name)
        for api_part in part_list:
            result, module_list= self.get_module_list(part_no=api_part["part_no"])
            api_part["module_list"] = module_list
        return True, part_list

    def get_module_list(self, part_no=None):
        cols = ["module_no", "module_name", "module_prefix", "module_desc", "module_part", "module_env"]
        module_list = self.db.execute_select(self.api_module, cols=cols, where_value=dict(module_part=part_no))
        return True, module_list

    def get_module_care_list(self, module_no):
        # 获得关注列表
        select_sql = "SELECT module_no,c.user_name,care_time,nick_name,level,email FROM sys_user as su,%s as c " \
                     "WHERE su.user_name=c.user_name AND module_no='%s';" % (self.module_care, module_no)
        self.db.execute(select_sql, auto_close=False)
        care_info = []
        for item in self.db.fetchall():
            care_info.append({"module_no": item[0], "user_name": item[1], "care_time": item[2].strftime(TIME_FORMAT),
                              "nick_name": item[3], "level": item[4], "email": item[5]})
        return care_info

    def get_api_basic_info(self, api_no):
        # get basic info
        basic_info_col = ("module_no", "api_no", "api_title", "api_path", "api_method", "api_desc", "add_time",
                          "update_time", "module_name", "module_prefix", "module_desc", "module_env", "stage")
        select_sql = "SELECT m.%s FROM %s AS i, api_module AS m WHERE i.module_no=m.module_no AND api_no='%s';" \
                     % (",".join(basic_info_col), self.api_info, api_no)
        result = self.db.execute(select_sql, auto_close=False)
        if result <= 0:
            return False, "Not Exist api_no"
        db_info = self.db.fetchone()
        basic_info = {}
        for i in range(len(db_info)):
            basic_info[basic_info_col[i]] = db_info[i]
        if basic_info["stage"] >= len(self.api_stage_desc) or basic_info["stage"] < 0:
            return False, "Not Exist api_no"
        basic_info["stage"] = self.api_stage_desc[basic_info["stage"]]
        basic_info["api_url"] = basic_info["module_prefix"].rstrip("/") + "/" + basic_info["api_path"].lstrip("/")
        basic_info["add_time"] = basic_info["add_time"].strftime(TIME_FORMAT) if basic_info["add_time"] is not None else ""
        basic_info["update_time"] = basic_info["update_time"].strftime(TIME_FORMAT) if basic_info["update_time"] is not None else ""
        return True, basic_info

    def get_api_example(self, api_no):
        cols = ["example_no", "api_no", "example_type", "example_desc", "example_content", "add_time"]
        db_items = self.db.execute_select(self.t_example, where_value=dict(api_no=api_no), cols=cols,
                                          order_by=["add_time"])
        return db_items

    def get_api_care_info(self, api_no):
        # 获得关注列表
        select_sql = "SELECT api_no,c.user_name,care_time,nick_name,level,email FROM sys_user as su,%s as c " \
                     "WHERE su.user_name=c.user_name AND api_no='%s';" % (self.api_care, api_no)
        self.db.execute(select_sql, auto_close=False)
        care_info = []
        for item in self.db.fetchall():
            care_info.append({"api_no": item[0], "user_name": item[1], "care_time": item[2].strftime(TIME_FORMAT),
                              "nick_name": item[3], "level": item[4], "email": item[5]})
        return care_info

    def get_api_info(self, api_no):
        if len(api_no) != 32:
            return False, "Bad api_no"
        where_value = dict(api_no=api_no)
        # get basic info
        result, basic_info = self.get_api_basic_info(api_no)
        if result is False:
            return False, basic_info
        # 获得请求头部参数列表
        cols = ["api_no", "param", "necessary", "param_desc"]
        header_info = self.db.execute_select(self.api_header, where_value=where_value, cols=cols, order_by=["add_time"])
        # 获得请求主体参数列表
        body_cols = ["api_no", "param", "necessary", "type", "param_desc", "status", "add_time", "update_time"]
        body_info = self.db.execute_select(self.api_body, where_value=dict(api_no=api_no), order_by=["add_time"],
                                           cols=body_cols)
        # 获得预定义参数列表
        cols = ["param", "param_type"]
        items = self.db.execute_select(self.predefine_param, cols=cols, where_value=where_value, order_by=["add_time"])
        predefine_param = {"header": [], "body": []}
        for item in items:
            if item["param_type"] in predefine_param:
                predefine_param[item["param_type"]].append(item["param"])
        # 获得预定义头部参数信息
        cols = ["param", "necessary", "param_desc"]
        items = self.db.execute_select(self.predefine_header, cols=cols)
        predefine_header = {}
        for item in items:
            predefine_header[item["param"]] = item
        # 获得预定义头部主体信息
        cols = ["param", "necessary", "type", "param_desc"]
        items = self.db.execute_select(self.predefine_body, cols=cols)
        predefine_body = {}
        for item in items:
            predefine_body[item["param"]] = item
        # 获得请求示例
        input_info = []
        # 获得返回示例
        output_info = []
        # 获得示例
        api_examples = self.get_api_example(api_no)
        for item in api_examples:
            if item["example_type"] == 1:
                input_info.append({"input_no": item["example_no"], "api_no": item["api_no"],
                                   "input_desc": item["example_desc"], "input_example": item["example_content"]})
            elif item["example_type"] == 2:
                output_info.append({"output_no": item["example_no"], "api_no": item["api_no"],
                                    "output_desc": item["example_desc"], "output_example": item["example_content"]})
        # 获得关注列表
        care_info = self.get_api_care_info(api_no)
        return True, {"basic_info": basic_info, "header_info": header_info, "body_info": body_info,
                      "input_info": input_info, "output_info": output_info, "care_info": care_info,
                      "predefine_param": predefine_param, "predefine_header": predefine_header,
                      "predefine_body": predefine_body, "examples": api_examples}

    def get_api_list(self, module_no):
        if type(module_no) != int:
            return False, "Bad module_no"
        cols = ["api_no", "module_no", "api_title", "api_path", "api_method", "api_desc", "stage", "add_time",
                "update_time"]
        order_by = ["stage", "api_path", "api_method"]
        items = self.db.execute_select(self.api_info, where_value=dict(module_no=module_no), order_by=order_by, cols=cols)
        api_list = []
        now_time = datetime.now()
        recent_seconds = 7 * 24 * 60 * 60
        for item in items:
            if item["stage"] >= len(self.api_stage_desc) or item["stage"] < 0 or item["stage"] >= 4:
                continue
            update_recent = False
            api_stage = self.api_stage_desc[item["stage"]]
            # if (now_time - item["add_time"]).total_seconds() < recent_seconds:
            #     update_recent = True
            # item["add_time"] = item["add_time"].strftime(TIME_FORMAT)
            # if item[8] is not None and (now_time - item[8]).total_seconds() < recent_seconds:
            #     update_recent = True
            # update_time = item[8].strftime(TIME_FORMAT) if item[8] is not None else ""
            item["update_recent"] = update_recent
            item["stage"] = api_stage
            api_list.append(item)
        care_info = self.get_module_care_list(module_no)
        return True, {"api_list": api_list, "care_info": care_info, "module_info": {"module_no": module_no}}

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
        where_value = {"api_no": api_no, "param": param}
        result = self.db.execute_delete(self.predefine_param, where_value)
        self.set_api_update(api_no)
        where_value["result"] = result
        return True, where_value

    def del_api_example(self, example_no):
        l = self.db.execute_delete(self.t_example, where_value=dict(example_no=example_no))
        return True, l

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
        self.set_api_stage(api_no, 5)
        update_sql = "UPDATE %s SET level=3 WHERE api_no='%s' AND user_name='%s';" \
                     % (self.api_care, api_no, user_name)
        self.db.execute(update_sql)
        return True, result

    def del_api_other_info(self, api_no):
        delete_sql_format = "DELETE FROM %s WHERE api_no='" + api_no + "';"
        for t in (self.api_header, self.t_example, self.api_body):
            delete_sql = delete_sql_format % t
            self.db.execute(delete_sql)
        return True, "success"


if __name__ == "__main__":
    api_help = HelpManager()
    api_help.get_test_env([2, 3])

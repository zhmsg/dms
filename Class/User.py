#! /usr/bin/env python
# coding: utf-8

import sys
import requests
from datetime import datetime
sys.path.append("..")
from Tools.Mysql_db import DB
from Check import check_char_num_underline as check_user, check_account_format
from Class import TIME_FORMAT, env

__author__ = 'ZhouHeng'

if env == "Development":
    jy_auth_host = "http://192.168.120.2:6011/auth"
else:
    jy_auth_host = "http://100.98.137.7/auth"


class UserManager:

    def __init__(self):
        self.db = DB()
        self.user = "sys_user"
        self.default_password = "gene.ac"
        self._data_role_desc = {"module_desc": u"数据传输", "role_list":  {
            "market": {"role_desc": u"市场", "role_value": 1},
            "upload": {"role_desc": u"上传", "role_value": 2},
            "calc": {"role_desc": u"计算", "role_value": 4} } }
        self._api_role_desc = {"module_desc": u"API文档", "role_list": {
            "api_look": {"role_desc": u"查看", "role_value": 8},
            "api_new": {"role_desc": u"新建", "role_value": 16},
            "api_module_new": {"role_desc": u"新建模块", "role_value": 8192 } } }
        self._table_role_desc = {"module_desc": u"数据表描述",
                                 "role_list": {"table_look": {"role_desc": u"查看", "role_value": 32} } }
        self._right_role_desc = {"module_desc": u"权限列表", "role_list": {
            "right_look": {"role_desc": u"查看", "role_value": 64},
            "right_new": {"role_desc": u"新建", "role_value": 16384} } }
        self._user_role_desc = {"module_desc": u"操作用户",
                                "role_list": {"user_new": {"role_desc": u"新建", "role_value": 128} } }
        self._bug_role_desc = {"module_desc": u"BUG操作", "role_list": {
            "bug_look": {"role_desc": u"查看", "role_value": 256},
            "bug_new": {"role_desc": u"新建", "role_value": 512},
            "bug_link": {"role_desc": u"被关联", "role_value": 1024},
            "bug_cancel": {"role_desc": u"取消", "role_value": 2048 },
            "bug_del": {"role_desc": u"删除", "role_value": 4096} } }
        self._status_code_role_desc = {"module_desc": u"API状态码", "role_list": {
            "status_code_look": {"role_desc": u"查看", "role_value": 32768},
            "status_code_new": {"role_desc": u"新建", "role_value": 65536},
            "status_code_del": {"role_desc": u"删除", "role_value": 131072},
            "status_code_module": {"role_desc": u"新建模块", "role_value": 524288} } }
        self._log_role_desc = {"module_desc": u"晶云平台日志", "role_list":
            {"log_look": {"role_desc": u"查看", "role_value": 262144},
             "log_receive": {"role_desc": u"接收", "role_value": 1048576} } }
        self._release_role_desc = {"module_desc": u"重新发布环境", "role_list":
            {"release_ih_N": {"role_desc": u"ih普通", "role_value": 2097152},
             "release_ih_V": {"role_desc": u"ihVIP", "role_value": 4194304},
             "release_ytj_N": {"role_desc": u"ytj普通", "role_value": 8388608}}}
        self.role_desc = {"data": self._data_role_desc, "api": self._api_role_desc, "table": self._table_role_desc,
                          "right": self._right_role_desc, "user": self._user_role_desc, "bug": self._bug_role_desc,
                          "status_code": self._status_code_role_desc, "log": self._log_role_desc,
                          "release": self._release_role_desc}
        self.__init_role__()

    def __init_role__(self):
        self.role_value = {}
        for key, role_module in self.role_desc.items():
            for role, value in role_module["role_list"].items():
                self.role_value[role] = value["role_value"]

    def new(self, user_name, role, nick_name, creator):
        if check_user(user_name, 1, 15) is False:
            return False, u"用户名只能由字母数字和下划线组成且长度不大于20"
        select_sql = "SELECT role FROM %s WHERE user_name='%s';" % (self.user, user_name)
        result = self.db.execute(select_sql)
        if result > 0:
            return False, u"用户名已存在"
        add_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (user_name,role,nick_name,creator,add_time) " \
                     "VALUES ('%s',%s,'%s','%s','%s');" \
                     % (self.user, user_name, role, nick_name, creator, add_time)
        self.db.execute(insert_sql)
        return True, user_name

    def check(self, user_name, password):
        check_url = "%s/confirm/" % jy_auth_host
        try:
            res = requests.post(check_url, json={"account": user_name, "password": password})
        except requests.ConnectionError as ce:
            return False, u"暂时无法登录，请稍后重试"
        r = res.json()
        if r["status"] != 1:
            return False, r["message"]
        select_sql = "SELECT user_name,role FROM %s WHERE user_name='%s';" % (self.user, r["data"]["account"])
        result = self.db.execute(select_sql)
        if result <= 0:
            r["data"]["role"] = 0
            return True, r["data"]
        db_r = self.db.fetchone()
        role = db_r[1]
        r["data"]["role"] = role
        return True, r["data"]

    def check_account_exist(self, user_name, check_name):
        if check_account_format(check_name) is False:
            return False, u"账户名仅允许数字和字母，下划线（_），而且必须以字母开头,用户名长度不得低于3位，不得高于20位"
        select_sql = "SELECT creator FROM %s WHERE user_name='%s';" % (self.user, check_name)
        result = self.db.execute(select_sql)
        if result > 0:
            if self.db.fetchone()[0] == user_name:
                return False, u"您已注册过该用户"
            return False, u"该用户已被他人注册"
        check_url = "%s/account/" % jy_auth_host
        try:
            res = requests.post(check_url, json={"list_account": [check_name]})
        except requests.ConnectionError as ce:
            return False, u"无法检测账户 ，请稍后重试"
        r = res.json()
        if r["status"] != 1:
            return False, r["message"]
        if len(r["data"]) == 1 and r["data"][0].lower() == check_name.lower():
            return True, r["data"][0]
        return False, u"账户名不存在"

    def change_password(self, user_name, old_password, new_password):
        change_url = "%s/password/" % jy_auth_host
        try:
            res = requests.put(change_url, json={"account": user_name, "password": old_password,
                                                  "new_password": new_password})
        except requests.ConnectionError as ce:
            return False, u"暂时无法更改密码，请稍后重试"
        r = res.json()
        if r["status"] != 2:
            return False, r["message"]
        return True, u"更新成功"

    def send_code(self, user_name, password, tel):
        change_url = "%s/code/bind/" % jy_auth_host
        try:
            res = requests.post(change_url, json={"account": user_name, "password": password, "tel": tel})
        except requests.ConnectionError as ce:
            return False, u"暂时无法发送，请稍后重试"
        r = res.json()
        if r["status"] == 2:
            return True, u"发送成功"
        if r["status"] == 10701:
            return False, u"请求频率过高，请稍后重试"
        if r["status"] == 10402:
            return False, u"手机号已被他人绑定，请更改还手机号"
        if r["status"] == 10801:
            return False, u"请求超过限制，请稍后重试"
        return False, r["message"]

    def bind_tel(self, user_name, password, tel, code):
        change_url = "%s/tel/" % jy_auth_host
        try:
            res = requests.post(change_url, json={"account": user_name, "password": password, "tel": tel, "code": code})
        except requests.ConnectionError as ce:
            return False, u"暂时绑定，请稍后重试"
        r = res.json()
        if r["status"] == 2:
            return True, u"绑定成功"
        if r["status"] == 10404:
            return False, u"验证码不正确，请重新输入"
        if r["status"] == 10405:
            return False, u"验证码已过期，请重新获得"
        if r["status"] == 10402:
            return False, u"手机号已被他人绑定，请更改还手机号"
        return False, r["message"]

    def clear_password(self, user_name, creator):
        update_sql = "UPDATE %s SET password=null WHERE user_name='%s' AND creator='%s';" % (self.user, user_name, creator)
        self.db.execute(update_sql)
        return True, u"重置成功"

    def get_role_user(self, role):
        cols = ["user_name", "role", "nick_name", "wx_id", "creator", "add_time", "email"]
        select_sql = "SELECT %s FROM %s WHERE role & %s > 0;" \
                     % (",".join(cols), self.user, role)
        self.db.execute(select_sql)
        user_list = []
        for item in self.db.fetchall():
            info = {}
            for i in range(len(cols)):
                info[cols[i]] = item[i]
            info["add_time"] = info["add_time"].strftime(TIME_FORMAT)
            user_list.append(info)
        return True, user_list

    def my_user(self, user_name):
        select_sql = "SELECT user_name,role,nick_name,wx_id,creator,add_time FROM %s WHERE creator='%s';" \
                     % (self.user, user_name)
        self.db.execute(select_sql)
        user_list = []
        for item in self.db.fetchall():
            user_list.append({"user_name": item[0], "role": item[1], "nick_name": item[2], "wx_id": item[3],
                              "creator": item[4], "add_time": item[5].strftime(TIME_FORMAT)})
        return True, user_list

    def get_user_info(self, user_name):
        select_sql = "SELECT user_name,role,nick_name,wx_id,creator,add_time,email FROM %s WHERE user_name='%s';" \
                     % (self.user, user_name)
        result = self.db.execute(select_sql)
        if result <= 0:
            return False, "user not exist"
        item = self.db.fetchone()
        user_info = {"user_name": item[0], "role": item[1], "nick_name": item[2], "wx_id": item[3], "creator": item[4],
                     "add_time": item[5], "email": item[6]}
        return True, user_info

    def update_my_user_role(self, role, user_name, my_name):
        if type(role) != int:
            return False, "Bad role"
        update_sql = "UPDATE %s SET role=%s WHERE user_name='%s' AND creator='%s';" \
                     % (self.user, role, user_name, my_name)
        self.db.execute(update_sql)
        return True, "success"

    def _add_role_my_user(self, role, user_name, my_name):
        if type(role) != int:
            return False, "Bad role"
        update_sql = "UPDATE %s SET role=role | %s WHERE user_name='%s' AND creator='%s';" \
                     % (self.user, role, user_name, my_name)
        self.db.execute(update_sql)
        return True, "success"

    def add_role_my_users(self, role, user_names, my_name):
        if type(user_names) != list:
            return "Bad user_names"
        if len(user_names) == 0:
            return True, "no update"
        if len(user_names) == 1:
            return self.add_role_my_user(role, user_names, my_name)
        if type(role) != int:
            return False, "Bad role"
        update_sql = "UPDATE %s SET role=role | %s WHERE creator='%s' AND user_name in ('%s');" \
                     % (self.user, role, "','".join(user_names), my_name)
        self.db.execute(update_sql)
        return True, "success"

    def _remove_role_my_user(self, role, user_name, my_name):
        if type(role) != int:
            return False, "Bad role"
        update_sql = "UPDATE %s SET role=role & ~%s WHERE user_name='%s' AND creator='%s';" \
                     % (self.user, role, user_name, my_name)
        self.db.execute(update_sql)
        return True, "success"

    def remove_role_my_users(self, role, user_names, my_name):
        if type(user_names) != list:
            return "Bad user_names"
        if len(user_names) == 0:
            return True, "no update"
        if len(user_names) == 1:
            return self.add_role_my_user(role, user_names, my_name)
        if type(role) != int:
            return False, "Bad role"
        update_sql = "UPDATE %s SET role=role & ~%s WHERE creator='%s' AND user_name in ('%s');" \
                     % (self.user, role, "','".join(user_names), my_name)
        self.db.execute(update_sql)
        return True, "success"


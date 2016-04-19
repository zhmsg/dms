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
    jy_auth_host = "http://10.51.72.158/auth"


class UserManager:

    def __init__(self):
        self.db = DB()
        self.user = "sys_user"
        self.default_password = "gene.ac"
        self.role_value = {"market": 1, "upload": 2, "calc": 4, "api_look": 8, "api_new": 16, "table_look": 32,
                           "right_look": 64, "user_new": 128, "bug_look": 256, "bug_new": 512, "bug_link": 1024,
                           "bug_cancel": 2048, "bug_del": 4096, "api_module_new": 8192, "right_new": 16384,
                           "status_code_look": 32768, "status_code_new": 65536, "status_code_del": 131072}

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
            res = None
        if res is None:
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
            res = None
        if res is None:
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

    def clear_password(self, user_name, creator):
        update_sql = "UPDATE %s SET password=null WHERE user_name='%s' AND creator='%s';" % (self.user, user_name, creator)
        self.db.execute(update_sql)
        return True, u"重置成功"

    def get_role_user(self, role):
        select_sql = "SELECT user_name,role,nick_name,wx_id,creator,add_time FROM %s WHERE role & %s > 0;" \
                     % (self.user, role)
        self.db.execute(select_sql)
        user_list = []
        for item in self.db.fetchall():
            user_list.append({"user_name": item[0], "role": item[1], "nick_name": item[2], "wx_id": item[3],
                              "creator": item[4], "add_time": item[5].strftime(TIME_FORMAT)})
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


#! /usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
sys.path.append("..")
from Tools.Mysql_db import DB
from Check import check_char_num_underline as check_user, check_password
from Class import TIME_FORMAT

__author__ = 'ZhouHeng'


class UserManager:

    def __init__(self):
        self.db = DB()
        self.user = "sys_user"
        self.user_desc = [
            ["user_name", "varchar(15)", "NO", "PRI", None, ""],
            ["password", "char(66)", "NO", "", None, ""],
            ["role", "tinyint(4)", "NO", "", None, ""],  # 1 代表可以市场部权限 2 代表具有上传者权限 4 代表具有计算者权限
                                                        # 8 代表可以查看API帮助文档 16 代表可以添加API帮助文档
                                                        # 32 代表可以查看数据库表设计 64 代表可以查看权限设计
                                                        # 128代表新建和更新用户的权限
                                                        # 256 代表有查看BUG列表权限 512 代表有新建BUG的权限
                                                        # 1024 代表被关联BUG的权限 2048 代表有取消他人BUG的权限
            ["nick_name", "varchar(20)", "NO", "", None, ""],
            ["wx_id", "char(28)", "NO", "", None, ""],
            ["creator", "varchar(15)", "NO", "", None, ""],
            ["add_time", "datetime", "NO", "", None, ""]
        ]
        self.default_password = "gene.ac"
        self.role_value = {"market": 1, "upload": 2, "calc": 4, "api_look": 8, "api_new": 16, "table_look": 32,
                           "auth_look": 64, "user_new": 128, "bug_look": 256, "bug_new": 512, "bug_link": 1024,
                           "bug_cancel": 2048}

    def create_user(self, force=False):
        return self.db.create_table(self.user, self.user_desc, force)

    def check_user(self):
        return self.db.check_table(self.user, self.user_desc)

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
        if check_user(user_name, 1, 15) is False:
            return False, u"用户名只能由字母数字和下划线组成且长度不大于15"
        if check_password(password, 1, 20) is False:
            return False, u"密码只能由字母数字和下划线@组成且长度不大于20"
        select_sql = "SELECT user_name,password,role FROM %s WHERE user_name='%s';" % (self.user, user_name)
        result = self.db.execute(select_sql)
        if result <= 0:
            return False, u"用户名不存在"
        db_r = self.db.fetchone()
        en_password = db_r[1]
        role = db_r[2]
        if en_password is None or en_password == "":
            if password == self.default_password:
                return True, -1
            else:
                return False, u"密码不正确"
        if check_password_hash(en_password, password) is False:
            return False, u"密码不正确"
        return True, role

    def change_password(self, user_name, new_password):
        if check_password(new_password, 1, 20) is False:
            return False, u"密码只能由字母数字和下划线@组成且长度不大于20"
        en_password = generate_password_hash(new_password)
        update_sql = "UPDATE %s SET password='%s' WHERE user_name='%s';" % (self.user, en_password, user_name)
        self.db.execute(update_sql)
        return True, u"更新成功"

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


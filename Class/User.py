#! /usr/bin/env python
# coding: utf-8

import sys
from werkzeug.security import generate_password_hash, check_password_hash
sys.path.append("..")
from Tools.Mysql_db import DB
from Check import check_char_num_underline as check_user, check_password

__author__ = 'ZhouHeng'


class UserManager:

    def __init__(self):
        self.db = DB()
        self.user = "sys_user"
        self.user_desc = [
            ["user_name", "varchar(15)", "NO", "PRI", None, ""],
            ["password", "char(66)", "NO", "", None, ""],
            ["role", "tinyint(4)", "NO", "", None, ""],  # 1代表可以市场部权限 2代表具有上传者权限 4代表具有计算者权限
                                                        # 8代表可以查看API帮助文档 16代表可以添加API帮助文档
                                                        # 32代表可以查看数据库表设计 64代表可以查看权限设计
            ["nick_name", "varchar(20)", "NO", "", None, ""]
        ]

    def create_user(self, force=False):
        return self.db.create_table(self.user, self.user_desc, force)

    def check_user(self):
        return self.db.check_table(self.user, self.user_desc)

    def new(self, user_name, password, role, nick_name):
        if check_user(user_name, 1, 15) is False:
            return False, u"用户名只能由字母数字和下划线组成且长度不大于20"
        select_sql = "SELECT role FROM %s WHERE user_name='%s';" % (self.user, user_name)
        result = self.db.execute(select_sql)
        if result > 0:
            return False, u"用户名已存在"
        if check_password(password, 1, 20) is False:
            return False, u"密码只能由字母数字和下划线组成且长度不大于20"
        en_password = generate_password_hash(password)
        insert_sql = "INSERT INTO %s (user_name,password,role,nick_name) VALUES ('%s','%s',%s,'%s');" \
                     % (self.user, user_name, en_password, role, nick_name)
        self.db.execute(insert_sql)
        return True, user_name

    def check(self, user_name, password):
        if check_user(user_name, 1, 15) is False:
            return False, u"用户名只能由字母数字和下划线组成且长度不大于15"
        if check_password(password, 1, 20) is False:
            return False, u"密码只能由字母数字和下划线组成且长度不大于15"
        select_sql = "SELECT user_name,password,role FROM %s WHERE user_name='%s';" % (self.user, user_name)
        result = self.db.execute(select_sql)
        if result <= 0:
            return False, u"用户名不存在"
        db_r = self.db.fetchone()
        en_password = db_r[1]
        role = db_r[2]
        if check_password_hash(en_password, password) is False:
            return False, u"密码不正确"
        return True, role

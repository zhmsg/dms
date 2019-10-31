# !/usr/bin/env python
# coding: utf-8

import base64
import hashlib
import os
import re
import time
from werkzeug.security import generate_password_hash, check_password_hash

from dms.objects.base import DBObject


class UserObject(DBObject):
    """
    role
    11 超级管理员 授权管理员
    10 管理员 可访问任意模块
    ...
    1  默认普通用户 根据模块权限访问模块

    """
    _salt_password = "msg_zh2018"

    @staticmethod
    def _md5_hash(s):
        m = hashlib.md5()
        if isinstance(s, str) is True:
            s = s.encode("utf-8")
        m.update(s)
        return m.hexdigest()

    @staticmethod
    def _md5_hash_password(user_name, password):
        md5_password = UserObject._md5_hash(user_name + password + user_name)
        return (md5_password + UserObject._salt_password).upper()

    @staticmethod
    def _password_check(password, db_password, user_name):
        if db_password is None:
            return False  # 密码为空 无限期禁止登录
        if len(password) <= 20:
            _md5_p = UserObject._md5_hash_password(user_name, password)
            if check_password_hash(db_password, _md5_p) is True:
                return True
        return False

    def __init__(self):
        DBObject.__init__(self)
        self.t = "sys_user"

    # 插入用户注册数据
    def insert_user(self, user_name=None, password=None, tel=None,
                    nick_name=None, email=None, wx_id=None, creator=None,
                    role=1):
        add_time = int(time.time())
        if nick_name is not None:
            if isinstance(nick_name, str):
                nick_name = nick_name.encode("utf-8")
            nick_name = base64.b64encode(nick_name)
        kwargs = dict(user_name=user_name, password=password, tel=tel,
                      nick_name=nick_name, email=email, wx_id=wx_id,
                      creator=creator, add_time=add_time, role=role)
        if password is not None:
            _md5_p = self._md5_hash_password(user_name, password)
            kwargs["password"] = generate_password_hash(_md5_p)
        l = self.db.execute_insert(self.t, kwargs=kwargs, ignore=True)
        return l

    def update_password(self, user_name, new_password):
        _md5_p = self._md5_hash_password(user_name, new_password)
        en_password = generate_password_hash(_md5_p)
        update_value = {"password": en_password}
        result = self.db.execute_update(self.t, update_value=update_value,
                                        where_value={"user_name": user_name})
        return result

    def _update_user(self, user_no, **update_value):
        allow_keys = ["nick_name", "avatar_url"]
        for key in update_value:
            if key not in allow_keys:
                del update_value[key]
        if "nick_name" in update_value:
            nick_name = update_value["nick_name"]
            if isinstance(nick_name, str):
                nick_name = nick_name.encode("utf-8")
            update_value["nick_name"] = base64.b64encode(nick_name)
        l = self.db.execute_update(self.t, update_value=update_value,
                                   where_value=dict(user_no=user_no))
        return l

    # 验证auth是否存在 包括 account tel alias wx_id
    def verify_user_exist(self, **kwargs):
        cols = ["user_no", "user_name", "tel", "email", "wx_id", "role",
                "nick_name", "avatar_url"]
        if kwargs.pop("need_password", None) is not None:
            cols.append("password")
        db_items = self.db.execute_select(self.t, where_value=kwargs,
                                          cols=cols, package=True)
        for u_item in db_items:
            try:
                u_item["nick_name"] = base64.b64decode(u_item["nick_name"])
            except Exception as e:
                print(e)
        return db_items

    def new_user(self, user_name, password=None, nick_name=None,
                 creator=None, role=1):
        items = self.verify_user_exist(user_name=user_name)
        if len(items) > 0:
            return False, u"用户名已存在"
        if nick_name is None:
            nick_name = user_name
        self.insert_user(user_name, password, nick_name=nick_name,
                         creator=creator, role=role)
        return True, dict(user_name=user_name)

    def new_wx_user(self, wx_id):
        self.insert_user(wx_id=wx_id)
        items = self.verify_user_exist(wx_id=wx_id)
        if len(items) <= 0:
            return None
        return items[0]

    def user_confirm(self, password, user_no=None, user_name=None,
                     email=None, tel=None, user=None):
        if user_no is not None:
            where_value = dict(user_no=user_no)
        elif user_name is not None:
            where_value = dict(user_name=user_name)
        elif email is not None:
            where_value = {"email": email}
        elif tel is not None:
            where_value = {"tel": tel}
        elif user is not None:
            if re.match(r"\d{1,10}$", user) is not None:
                where_value = dict(user_no=user)
            elif re.match(r"1\d{10}$", user) is not None:
                where_value = {"tel": user}
            elif re.match(r"\S+@\s+$", user) is not None:
                where_value = dict(email=user)
            else:
                where_value = dict(user_name=user)
        else:
            return -3, None
        where_value["need_password"] = True
        db_items = self.verify_user_exist(**where_value)
        if len(db_items) <= 0:
            return -2, None
        user_item = db_items[0]
        account = user_item["user_name"]
        db_password = user_item["password"]
        if self._password_check(password, db_password, account) is False:
            return -1, None
        del user_item["password"]
        return 0, user_item

    def update_info(self, user_no, **kwargs):
        l = self._update_user(user_no, **kwargs)
        return l

    def get_multi_nick_name(self, user_list):
        cols = ["user_no", "nick_name", "avatar_url"]
        user_list = set(user_list)
        items = self.db.execute_multi_select(self.t, where_value=dict(user_no=user_list), cols=cols)
        for u_item in items:
            try:
                u_item["nick_name"] = base64.b64decode(u_item["nick_name"])
            except Exception as e:
                print(e)
        return items


if __name__ == "__main__":
    user = UserObject()
    user.new_user("admin", "admin")

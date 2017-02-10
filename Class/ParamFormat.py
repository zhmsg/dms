#! /usr/bin/env python
# coding: utf-8

from time import time
from Tools.Mysql_db import DB


__author__ = 'ZhouHeng'


class ParamFormatManager:

    def __init__(self):
        self.db = DB()
        self.t_param_format = "param_format"

    def new_param_format(self, user_name, param, param_type, **kwargs):
        cols = ["min_len", "max_len", "not_allow", "match_str", "param_desc"]
        now_time = int(time())
        sql_args = dict(add_user=user_name, param=param, param_type=param_type, add_time=now_time, update_time=now_time,
                        update_user=user_name)
        for col_item in cols:
            if col_item in kwargs:
                sql_args[col_item] = kwargs[col_item]
        result = self.db.execute_insert(self.t_param_format, args=sql_args, ignore=True)
        return True, sql_args

    def update_param_format(self, user_name, param, **kwargs):
        cols = ["param_type", "min_len", "max_len", "not_allow", "match_str", "param_desc"]
        sql_args = dict(update_user=user_name, update_time=int(time()))
        for col_item in cols:
            if col_item in kwargs:
                sql_args[col_item] = kwargs[col_item]
        result = self.db.execute_update(self.t_param_format, update_value=sql_args, where_value={"param": param})
        sql_args["param"] = param
        return True, sql_args

    def select_param_format(self):
        cols = ["param", "param_type", "min_len", "max_len", "not_allow", "match_str", "param_desc"]
        params_info = self.db.execute_select(self.t_param_format, cols=cols, package=True)
        return True, params_info

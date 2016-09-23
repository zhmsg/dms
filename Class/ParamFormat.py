#! /usr/bin/env python
# coding: utf-8

from Tools.Mysql_db import DB


__author__ = 'ZhouHeng'


class ParamFormatManager:

    def __init__(self):
        self.db = DB()
        self.t_param_format = "param_format"

    def new_param_format(self, param, param_type, **kwargs):
        cols = ["min_len", "max_len", "not_allow", "match_str", "param_desc"]
        sql_args = dict(param=param, param_type=param_type)
        for col_item in cols:
            if col_item in kwargs:
                sql_args[col_item] = kwargs[col_item]
        result = self.db.execute_insert(self.t_param_format, args=sql_args, ignore=True)
        return True, result

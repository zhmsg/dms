#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from time import time
from Tools.Mysql_db import DB


class OthersManager(object):

    def __init__(self):
        self.db = DB()
        self.t_others_r = "others_result"

    def insert_others_info(self, other_type, result_info):
        insert_time = int(time())
        result_no = int(time() * 1000)
        kwargs = dict(result_no=result_no, other_type=other_type, result_info=result_info, insert_time=insert_time)
        l = self.db.execute_insert(self.t_others_r, kwargs=kwargs)
        return True, l

    def select_others_info(self, other_type):
        where_value = {"other_type": other_type}
        cols = ["result_no", "other_type", "result_info", "insert_time"]
        db_items = self.db.execute_select(self.t_others_r, where_value=where_value, cols=cols, package=True)
        return True, db_items



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
        kwargs = dict(other_type=other_type, result_info=result_info, insert_time=insert_time)
        l = self.db.execute_insert(self.t_others_r, args=kwargs)
        return True, l

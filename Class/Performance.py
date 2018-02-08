#! /usr/bin/env python
# coding: utf-8

import os
from time import time
import hashlib
from JYTools.DB import DB
from Class import conf_dir

__author__ = 'ZhouHeng'


class PerformanceManager(object):

    def __init__(self):
        self.db = DB(conf_path=os.path.join(conf_dir, "mysql_dms.conf"))
        self.t = "performance"
        self.t_module_related = "performance_module_related"
        self.t_members = "performance_members"

    def insert_performance(self, name, detail_info, start_time, end_time, user_name):
        data = dict(name=name, detail_info=detail_info, start_time=start_time, end_time=end_time, adder=user_name)
        data["insert_time"] = int(time())
        m = hashlib.md5()
        m.update(detail_info)
        data["id"] = m.hexdigest()
        l = self.db.execute_insert(self.t, data, ignore=True)
        if l > 0:
            return data
        return None

    def insert_module_related(self, month, module_no, performance_id):
        data = dict(month=month, module_no=module_no, id=performance_id)
        l = self.db.execute_insert(self.t_module_related, data, ignore=True)
        if l > 0:
            return data
        return None

    def insert_members(self, performance_id, user_name, score):
        data = dict(id=performance_id, user_name=user_name, score=score)
        l = self.db.execute_insert(self.t_members, data, ignore=True)
        if l > 0:
            return data
        return None

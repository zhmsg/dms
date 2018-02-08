#! /usr/bin/env python
# coding: utf-8

import os
import datetime
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

    @staticmethod
    def get_months():
        now_time = datetime.datetime.now()
        now_month = "%s%s" % (now_time.year, str(now_time.month).zfill(2))
        if now_time.month == 1:
            last_month = "%s%s" % (now_time.year - 1, 12)
        else:
            last_month = "%s%s" % (now_time.year, str(now_time.month - 1).zfill(2))
        return [now_month, last_month]

    def get_performance(self, months=None):
        if months is None:
            months = self.get_months()
        r_cols = ["month", "module_no", "id"]
        r_items = self.db.execute_multi_select(self.t_module_related, where_value=dict(month=months), cols=r_cols)
        ids = map(lambda x: x["id"], r_items)
        p_cols = ["id", "name", "detail_info", "start_time"]
        p_items = self.db.execute_multi_select(self.t, where_value=dict(id=ids), cols=p_cols)
        m_cols = ["id", "user_name", "score"]
        m_items = self.db.execute_multi_select(self.t_members, where_value=dict(id=ids), cols=m_cols)
        return r_items, p_items, m_items

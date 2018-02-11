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
    def get_months(only_last=False):
        now_time = datetime.datetime.now()
        now_month = "%s%s" % (now_time.year, str(now_time.month).zfill(2))
        if now_time.month == 1:
            last_month = "%s%s" % (now_time.year - 1, 12)
        else:
            last_month = "%s%s" % (now_time.year, str(now_time.month - 1).zfill(2))
        if only_last is True:
            return [last_month]
        return [now_month, last_month]

    def get_performance(self, months=None):
        if isinstance(months, unicode) is True:
            if len(months) != 6:
                months = None
            else:
                months = [months]
        if months is None or len(months) == 0:
            months = self.get_months()
        r_cols = ["month", "module_no", "id"]
        r_items = self.db.execute_multi_select(self.t_module_related, where_value=dict(month=months), cols=r_cols,
                                               order_by=["id"])
        ids = map(lambda x: x["id"], r_items)
        if len(ids) <= 0:
            return []
        p_cols = ["id", "name", "detail_info", "start_time", "end_time"]
        p_items = self.db.execute_multi_select(self.t, where_value=dict(id=ids), cols=p_cols)
        pr_items = []
        pi = 0
        ri = 0
        while ri < len(r_items) and pi < len(p_items):
            if r_items[ri]["id"] == p_items[pi]["id"]:
                r_items[ri].update(p_items[pi])
                r_items[ri]["members"] = []
                pr_items.append(r_items[ri])
                pi += 1
                ri += 1
            elif r_items[ri]["id"] > p_items[pi]["id"]:
                pi += 1
            else:
                ri += 1
        m_cols = ["id", "user_name", "score"]
        m_items = self.db.execute_multi_select(self.t_members, where_value=dict(id=ids), cols=m_cols)
        pri = 0
        mi = 0
        while pri < len(pr_items) and mi < len(m_items):
            if pr_items[pri]["id"] == m_items[mi]["id"]:
                pr_items[pri]["members"].append(m_items[mi])
                mi += 1
            elif pr_items[pri]["id"] > m_items[mi]["id"]:
                mi += 1
            else:
                pri += 1
        return pr_items

#! /usr/bin/env python
# coding: utf-8

import sys
from Tools.Mysql_db import DB, DBItem

__author__ = 'ZhouHeng'


class JingDuDataManager(object):

    def __init__(self, mysql_host, mysql_db):
        self.db = DB(host=mysql_host, mysql_user="gener", mysql_password="gene_ac252", mysql_db=mysql_db)
        self.t_sys_projects = "sys_projects"
        self.t_project_user = "project_user_right"
        self.t_sys_samples = "sys_samples"
        self.t_sample_user = "sample_user_right"
        self.t_sample_info = "sample_info"
        self.t_project_sample = "sys_project_sample"
        self.db_user_task = DBItem("user_task_list", db=self.db)
        self.db_app = DBItem("app_list", db=self.db)

    def _select_project(self, where_value=None, limit_num=20):
        cols = ["project_no", "project_name", "description", "date_created", "display_level", "completed", "lastModify",
                "portal"]
        mul_p_info = self.db.execute_select(self.t_sys_projects, cols=cols, package=True, order_by=["project_no"],
                                            order_desc=True, limit=limit_num, where_value=where_value)
        return True, mul_p_info

    def select_project(self, project_no=None):
        where_value = None
        if project_no is not None:
            if not isinstance(project_no, int):
                return False, "错误的项目编号"
            where_value = dict(project_no=project_no)
        return self._select_project(where_value)

    def _select_project_user(self, where_value=None, limit_num=20):
        cols = ["project_no", "account", "role", "date_added"]
        mul_pu_info = self.db.execute_select(self.t_project_user, cols=cols, package=True, order_by=["sys_no"],
                                             order_desc=True, where_value=where_value, limit=limit_num)
        return True, mul_pu_info

    def select_project_user(self, project_no=None, account=None):
        where_value = dict()
        if project_no is not None:
            if not isinstance(project_no, int):
                return False, "错误的项目编号"
            where_value.update(dict(project_no=project_no))
        elif account is not None:
            where_value.update(dict(account=account))
        else:
            return False, "必须传入项目号或者账户名"
        return self._select_project_user(where_value)

    def _select_sample(self, where_value=None, limit_num=20):
        cols = ["sample_no", "sample_id", "patient_no", "date_created", "display_level", "portal", "status_tag",
                "ref_sample"]
        mul_s_info = self.db.execute_select(self.t_sys_samples, cols=cols, package=True, order_by=["sample_no"],
                                            order_desc=True, where_value=where_value, limit=limit_num)
        return True, mul_s_info

    def select_sample(self, sample_no=None):
        where_value = None
        if sample_no is not None:
            if not isinstance(sample_no, int):
                return False, "错误的样本编号"
            where_value = dict(sample_no=sample_no)
        return self._select_sample(where_value)

    def _select_sample_info(self, where_value=None, limit_num=20):
        cols = ["sample_no", "stage", "completed_time_1", "completed_time_2", "completed_time_3", "completed_time_4",
                "diagnosis", "sample_type", "seq_type", "seq_files"]
        mul_si_info = self.db.execute_select(self.t_sample_info, cols=cols, package=True, order_by=["sample_no"],
                                             order_desc=True, where_value=where_value, limit=limit_num)
        return True, mul_si_info

    def select_sample_info(self, sample_no):
        if not isinstance(sample_no, int):
            return False, "错误的样本编号"
        where_value = dict(sample_no=sample_no)
        return self._select_sample_info(where_value)

    def _select_sample_user(self, where_value=None, limit_num=20):
        cols = ["sys_no", "sample_no", "account", "role"]
        mul_su_info = self.db.execute_select(self.t_sample_user, cols=cols, package=True, order_by=["sys_no"],
                                             order_desc=True, where_value=where_value, limit=limit_num)
        return True, mul_su_info

    def select_sample_user(self, sample_no=None, account=None):
        where_value = dict()
        if sample_no is not None:
            if not isinstance(sample_no, int):
                return False, "错误的样本编号"
            where_value.update(dict(sample_no=sample_no))
        elif account is not None:
            where_value.update(dict(account=account))
        else:
            return False, "必须传入账户名"
        return self._select_sample_user(where_value)

    def select_task(self, task_id=None, app_id=None, account=None, started_stamp=None, **kwargs):
        cols = ["task_id", "app_id", "account", "input", "output", "status", "db_status", "started_stamp",
                "finished_stamp"]
        where_value = dict()
        where_cond = []
        if task_id is not None:
            where_value["task_id"] = task_id
        if app_id is not None:
            where_value["app_id"] = app_id
        if account is not None:
            where_value["account"] = account
        if started_stamp is not None:
            where_cond.append("started_stamp>=%s" % started_stamp)
        if kwargs.get("s_status", None) is not None:
            where_cond.append("status>=%s" % kwargs["s_status"])
        if kwargs.get("e_status", None) is not None:
            where_cond.append("status<=%s" % kwargs["e_status"])
        db_items = self.db_user_task.execute_select(cols=cols, where_value=where_value, where_cond=where_cond, **kwargs)
        return True, db_items

    def select_app_list(self):
        cols = ["app_id", "app_name", "app_desc", "status_desc"]
        db_items = self.db_app.execute_select(cols=cols)
        return True, db_items

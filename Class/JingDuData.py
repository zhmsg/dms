#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB

__author__ = 'ZhouHeng'


class JingDuDataManager(object):

    def __init__(self, mysql_host, mysql_db):
        self.db = DB(host=mysql_host, mysql_user="gener", mysql_password="gene_ac252", mysql_db=mysql_db)
        self.t_sys_projects = "sys_projects"
        self.t_project_user = "project_user_right"

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
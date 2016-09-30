#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import sys
from fabric.api import *
from datetime import datetime
from time import time
sys.path.append("..")
from Tools.Mysql_db import DB


class PullRequestManager:

    def __init__(self):
        self.db = DB()
        self.t_git_hub = "github_pull_request"

    def add_pull_request(self, **kwargs):
        request_info = dict(action_no=int(time()))
        request_info["request_num"] = kwargs["request_num"]
        request_info["action_user"] = kwargs["action_user"][:50]
        request_info["request_title"] = kwargs["request_title"][:100]
        request_info["request_body"] = kwargs["request_body"][:300]
        request_info["base_branch"] = kwargs["base_branch"][:50]
        request_info["compare_branch"] = kwargs["compare_branch"][:50]
        request_info["merged"] = kwargs["merged"]
        request_info["repository"] = kwargs["repository"][:50]
        self.db.execute_insert(self.t_git_hub, args=request_info)
        return True

    def select_pull_request(self, action_no=None, **kwargs):
        cols = ["action_no", "request_num", "action_user", "request_title", "request_body", "base_branch",
                "compare_branch", "merged", "repository"]
        select_sql = "SELECT %s FROM %s" % (",".join(cols), self.t_git_hub)
        where_con = []
        if action_no is not None:
            where_con.append("action_no>=%s" % action_no)
        for key in kwargs:
            where_con.append("{0}=%({0})s".format(key))
        if len(where_con) > 0:
            select_sql += " WHERE " + " AND ".join(where_con)
        select_sql += ";"
        self.db.execute(select_sql, args=kwargs)
        db_r = self.db.fetchall()
        pull_requests = []
        for item in db_r:
            p_info = {}
            for i in range(len(cols)):
                p_info[cols[i]] = item[i]
            p_info["merged"] = True if p_info["merged"] == "\x01" else False
            pull_requests.append(p_info)
        return True, pull_requests

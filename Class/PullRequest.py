#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import sys
from fabric.api import *
from datetime import datetime
from time import time
sys.path.append("..")
from Tools.Mysql_db import DB
from Class.WeiXin import WeiXinManager
from Class import TIME_FORMAT, wx_service, release_host, release_host_port


class PullRequestManager:

    def __init__(self):
        self.db = DB()
        self.t_git_hub = "github_pull_request"

    def add_pull_request(self, request_num, action_user, request_title, request_body, base_branch, compare_branch, merged, repository):
        action_no = int(time())
        info = dict(request_num=request_num, request_title=request_title, action_user=action_user,
                    request_body=request_body, base_branch=base_branch, compare_branch=compare_branch, merged=merged,
                    repository=repository, action_no=action_no)
        self.db.execute_insert(self.t_git_hub, args=info)
        return True

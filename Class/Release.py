#! /usr/bin/env python
# coding: utf-8

import sys
from fabric.api import *
from datetime import datetime
from time import time
sys.path.append("..")
from Tools.Mysql_db import DB
from Class import TIME_FORMAT


env.host_string = "10.51.72.158"

__author__ = 'ZhouHeng'


class ReleaseManager:

    def __init__(self):
        self.db = DB()
        self.release_task = "release_task"
        self.basic_time = datetime.strptime("2016-09-02 00:00:00", TIME_FORMAT)
        self.latest_branch = "master"

    def new_release_task(self, user_name, reason, reason_desc):
        release_time = datetime.now() - self.basic_time
        release_no = release_time.seconds / 3600 + release_time.days * 24
        status_info = "%s1" % int(time())
        args = dict(release_no=release_no, user_name=user_name, reason=reason, reason_desc=reason_desc,
                    status_info=status_info)
        result = self.db.execute_insert(self.release_task, args=args, ignore=True)
        if result <= 0:
            return False, u"任务已存在"
        return True, args

    def update_release_task(self, release_no, run_result=True):
        status_info = "|%s%s" % (int(time()), 1 if run_result is True else 0)
        update_sql = "UPDATE %s SET status_info=CONCAT(status_info, '%s') WHERE release_no=%s;" \
                     % (self.release_task, status_info, release_no)
        self.db.execute(update_sql)
        return True, "success"

    def select_release_task(self, user_name=None):
        release_time = datetime.now() - self.basic_time
        min_release_no = release_time.days * 24
        cols = ["release_no", "user_name", "reason", "reason_desc", "status_info"]
        if user_name is None:
            zero = 1
        else:
            zero = 0
        select_sql = "SELECT %s FROM %s WHERE release_no>=%s AND (user_name='%s' OR %s) ORDER BY release_no DESC;" \
                     % (",".join(cols), self.release_task, min_release_no, user_name, zero)
        self.db.execute(select_sql)
        db_r = self.db.fetchall()
        task_list = []
        for item in db_r:
            task_info = {}
            for i in range(len(cols)):
                task_info[cols[i]] = item[i]
            task_list.append(task_info)
        return True, task_list

    def release_pull(self):
        with cd("/home/msg/BioMed"):
            run("git -c diff.mnemonicprefix=false -c core.quotepath=false fetch origin")
            run("git pull")
            run("git -c diff.mnemonicprefix=false -c core.quotepath=false pull --no-commit origin %s" % self.latest_branch)

    def release_commit(self):
        with cd("/home/msg/BioMed"):
            run("git commit '%s'" % "marge master")
            run("git push")



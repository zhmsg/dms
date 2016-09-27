#! /usr/bin/env python
# coding: utf-8

import sys
from fabric.api import *
from datetime import datetime
from time import time
sys.path.append("..")
from Tools.Mysql_db import DB
from Class.WeiXin import WeiXinManager
from Class import TIME_FORMAT, wx_service, release_host, release_host_port


env.host_string = release_host
env.port = release_host_port

__author__ = 'ZhouHeng'


class ReleaseManager:

    def __init__(self, release_dir):
        self.db = DB()
        self.release_task = "release_task"
        self.basic_time = datetime.strptime("2016-09-02 00:00:00", TIME_FORMAT)
        self.latest_branch = "master"
        self.api_work_dir = release_dir + "/ih_GATCAPI"
        self.wx = WeiXinManager(wx_service)

    def new_release_task(self, user_name, reason, restart_service, reason_desc):
        release_time = datetime.now() - self.basic_time
        release_no = release_time.seconds / 3600 + release_time.days * 24
        status_info = "%s1" % int(time())
        args = dict(release_no=release_no, user_name=user_name, reason=reason, restart_service=restart_service,
                    reason_desc=reason_desc, status_info=status_info)
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
        cols = ["release_no", "user_name", "restart_service", "reason", "reason_desc", "status_info"]
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

    def release_push_code(self, message):
        with cd(self.api_work_dir):
            run("git commit -m '%s'" % message, quiet=True)
            run("git push")

    def send_wx_msg(self, msg):
        result, user_list = self.wx.user_info()
        if result is False:
            return False, user_list
        for user_info in user_list:
            self.wx.send_status(u"后台开发", "ochiws2EiR0cq3qzXYjQkw0m9jdE", "Test", msg)
            break
            if user_info["groupid"] == 100:
                self.wx.send_status(u"后台开发", user_info["openid"], "Test", msg)
            elif user_info["groupid"] == 101:
                self.wx.send_status(u"前端开发", user_info["openid"], "Test", msg)
            elif user_info["groupid"] == 102:
                self.wx.send_status(u"产品设计", user_info["openid"], "Test", msg)
        return True, "success"

    def _restart_api(self):
        # 拉取代码
        with cd(self.api_work_dir):
            run("git stash && git fetch origin")
            run("git pull && git pull --no-commit origin %s" % self.latest_branch)
        with cd(self.api_work_dir):
            run('find -name "*.log" | xargs rm -rf')
            run("sh stop.sh")
            run('ssh service "sh /home/msg/GATCAPI/restart_service.sh"', quiet=True)
            run("sh start_api.sh")

    def release_ih(self):
        # 获得任务
        result, info = self.select_release_task()
        if result is False:
            return False, info
        if len(info) <= 0:
            return False, info
        release_time = datetime.now() - self.basic_time
        release_no = (release_time.seconds - 600) / 3600 + release_time.days * 24
        if info[0]["release_no"] != release_no:
            return False, "No Task"
        user_name = info[0]["user_name"]
        reason_desc = "%s %s\n%s" % (user_name, info[0]["reason"], info[0]["reason_desc"])
        restart_service = info[0]["restart_service"]
        print("start run release %s" % release_no)
        self.update_release_task(release_no, True)

        print("start restart")
        if restart_service == 1:
            self._restart_api()
        else:
            self.update_release_task(release_no, False)
            return False, "invalid restart service code"
        self.update_release_task(release_no, True)

        print("start test")
        self.update_release_task(release_no, True)

        print("start release push")
        self.release_push_code(reason_desc)
        self.update_release_task(release_no, True)
        self.send_wx_msg(reason_desc)
        return True, "success"





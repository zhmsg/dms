#! /usr/bin/env python
# coding: utf-8

import sys
from fabric.api import *
from datetime import datetime
from time import time
sys.path.append("..")
from Tools.Mysql_db import DB
from Class.WeiXin import WeiXinManager
from Class.Task import TaskManager
from Class.PullRequest import PullRequestManager
from Class import TIME_FORMAT, wx_service, release_host, release_host_port

__author__ = 'ZhouHeng'

env.host_string = release_host
env.port = release_host_port


def _push_code(work_dir, message):
    with cd(work_dir):
        run("git commit -m '%s'" % message, quiet=True)
        run("git push")


def _pull_code(work_dir, branch):
    # 拉取代码
    with cd(work_dir):
        run("git stash && git fetch origin")
        run("git pull && git pull --no-commit origin %s" % branch)


class ReleaseManager:

    def __init__(self, release_dir):
        self.db = DB()
        self.release_task = "release_task"
        self.basic_time = datetime.strptime("2016-09-02 00:00:00", TIME_FORMAT)
        self.latest_branch = "master"
        self.api_work_dir = release_dir + "/ih_GATCAPI"
        self.web_work_dir = release_dir + "/ih_GATCWeb"
        self.api_task = TaskManager(3)
        self.web_task = TaskManager(4)
        self.pull_request_man = PullRequestManager()
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

    def select_api_pull_request(self):
        result, scheduler_info = self.api_task.select_scheduler_status()
        task_status = scheduler_info["task_status"]
        return self.pull_request_man.select_pull_request(action_no=task_status, repository="GATCAPI", merged=True, base_branch="master")

    def select_web_pull_request(self):
        result, scheduler_info = self.web_task.select_scheduler_status()
        task_status = scheduler_info["task_status"]
        return self.pull_request_man.select_pull_request(action_no=task_status, repository="GATCWeb", merged=True, base_branch="master")

    def _restart_api(self):
        _pull_code(self.api_work_dir, self.latest_branch)
        with cd(self.api_work_dir):
            run('find -name "*.log" | xargs rm -rf')
            run("sh stop.sh")
            run('ssh service "sh /home/msg/GATCAPI/restart_service.sh"', quiet=True)
            run('nohup gunicorn -b 0.0.0.0:8100 -t 3600 -w 5 -k "gevent" --backlog 2048 -p "/tmp/api_gunicorn_test.pid" --chdir API run:app 1>> API.log 2>> API.log & sleep 3')
            run('cat /tmp/api_gunicorn_test.pid >> service.pid')
        self.api_task.update_scheduler_status(int(time()), "system", "restart ih api")

    def _restart_web(self):
        _pull_code(self.web_work_dir, self.latest_branch)
        with cd(self.web_work_dir):
            run('find -name "*.log" | xargs rm -rf')
            run("sh stop.sh")
            run('nohup gunicorn -b 0.0.0.0:9101 -t 3600 -w 5 -k "gevent" --backlog 2048 -p "/tmp/web_gunicorn_test.pid" --chdir Web2 Webstart:app 1>> WEB.log 2>> WEB.log & sleep 3')
            run('cat /tmp/web_gunicorn_test.pid >> service.pid')
        self.web_task.update_scheduler_status(int(time()), "system", "restart ih web")

    def _release_api(self, user_name, release_no, reason, reason_desc):
        reason_desc = u"%s 重启API测试环境 %s\n%s\n" % (user_name, reason, reason_desc)
        wx_msg = reason_desc
        # 获得提交的pull request信息
        result, pull_requests = self.select_api_pull_request()
        if len(pull_requests) <= 0:
            return False, u"API无更新"
        else:
            wx_msg += u"API更新如下:\n"
            for i in range(len(pull_requests) - 1, -1, -1):
                wx_msg += u"%s、%s\n" % (i+1, pull_requests[i]["request_title"])
        print("start restart")
        self._restart_api()
        self.update_release_task(release_no, True)
        print("start test")
        self.update_release_task(release_no, True)
        print("start push")
        _push_code(self.api_work_dir, reason_desc)
        self.update_release_task(release_no, True)
        self.send_wx_msg(wx_msg)
        return True, "success"

    def _release_web(self, user_name, release_no, reason, reason_desc):
        reason_desc = u"%s 重启WEB测试环境 %s\n%s\n" % (user_name, reason, reason_desc)
        wx_msg = reason_desc
        # 获得提交的pull request信息
        result, pull_requests = self.select_web_pull_request()
        if len(pull_requests) <= 0:
            return False, u"WEB无更新"
        else:
            wx_msg += u"WEB更新如下:\n"
            for i in range(len(pull_requests) - 1, -1, -1):
                wx_msg += u"%s、%s\n" % (i+1, pull_requests[i]["request_title"])
        print("start restart")
        self._restart_web()
        self.update_release_task(release_no, True)
        print("start test")
        self.update_release_task(release_no, True)
        print("start push")
        _push_code(self.web_work_dir, reason_desc)
        self.update_release_task(release_no, True)
        self.send_wx_msg(wx_msg)
        return True, "success"

    def _release_ih(self, user_name, release_no, reason, reason_desc):
        reason_desc = u"%s 重启API&WEB测试环境 %s\n%s\n" % (user_name, reason, reason_desc)
        wx_msg = reason_desc
        # 获得提交的pull request信息
        result, pull_requests = self.select_web_pull_request()
        if len(pull_requests) <= 0:
            return False, u"WEB无更新"
        else:
            wx_msg += u"WEB更新如下:\n"
            for i in range(len(pull_requests) - 1, -1, -1):
                wx_msg += u"%s、%s\n" % (i+1, pull_requests[i]["request_title"])
        result, pull_requests = self.select_api_pull_request()
        if len(pull_requests) <= 0:
            return False, u"API无更新"
        else:
            wx_msg += u"API更新如下:\n"
            for i in range(len(pull_requests) - 1, -1, -1):
                wx_msg += u"%s、%s\n" % (i+1, pull_requests[i]["request_title"])
        print("start restart")
        self._restart_api()
        self._restart_web()
        self.update_release_task(release_no, True)
        print("start test")
        self.update_release_task(release_no, True)
        print("start push")
        _push_code(self.api_work_dir, reason_desc)
        _push_code(self.web_work_dir, reason_desc)
        self.update_release_task(release_no, True)
        self.send_wx_msg(wx_msg)
        return True, "success"

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
        restart_service = info[0]["restart_service"]
        user_name = info[0]["user_name"]
        reason = info[0]["reason"]
        reason_desc = info[0]["reason_desc"]
        print("start run release %s" % release_no)
        self.update_release_task(release_no, True)

        if restart_service == 0:
            return self._release_ih(user_name, release_no, reason, reason_desc)
        elif restart_service == 1:
            return self._release_api(user_name, release_no, reason, reason_desc)
        elif restart_service == 2:
            return self._release_web(user_name, release_no, reason, reason_desc)
        else:
            return False, "invalid restart service code"


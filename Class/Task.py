#! /usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime, timedelta
from time import time
from Tools.Mysql_db import DB


__author__ = 'ZhouHeng'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TaskManager(object):

    def __init__(self, task_type):
        self.db = DB()
        self.register_task = "register_task"
        self.scheduler_status = "task_scheduler_status"
        self.task_type = task_type

    def register_new_task(self, task_no, user_name, reason, reason_desc):
        status_info = "%s1" % int(time())
        args = dict(task_no=task_no, task_type=self.task_type, user_name=user_name, reason=reason,
                    reason_desc=reason_desc, status_info=status_info)
        result = self.db.execute_insert(self.register_task, kwargs=args, ignore=True)
        if result <= 0:
            return False, result
        return True, args

    def update_register_task(self, task_no, run_result=True):
        status_info = "|%s%s" % (int(time()), 1 if run_result is True else 0)
        update_sql = "UPDATE %s SET status_info=CONCAT(status_info, '%s') WHERE task_no=%s AND task_type=%s;" \
                     % (self.register_task, status_info, task_no, self.task_type)
        self.db.execute(update_sql)
        return True, "success"

    def select_register_task(self, task_no, user_name=None):
        cols = ["task_no", "task_type", "user_name", "reason", "reason_desc", "status_info"]
        if user_name is None:
            zero = 1
        else:
            zero = 0
        select_sql = "SELECT %s FROM %s WHERE task_no>=%s AND task_type=%s AND (user_name='%s' OR %s) " \
                     "ORDER BY task_no DESC;" \
                     % (",".join(cols), self.register_task, task_no, self.task_type, user_name, zero)
        self.db.execute(select_sql)
        db_r = self.db.fetchall()
        task_list = []
        for item in db_r:
            task_info = {}
            for i in range(len(cols)):
                task_info[cols[i]] = item[i]
            task_list.append(task_info)
        return True, task_list

    def _new_task_status(self, task_status, user_name, reason_desc):
        update_time = int(time())
        args = dict(task_type=self.task_type, task_status=task_status, user_name=user_name, reason_desc=reason_desc,
                    update_time=update_time)
        result = self.db.execute_insert(self.scheduler_status, kwargs=args)
        return True, result

    def update_scheduler_status(self, task_status, user_name, reason_desc):
        update_time = int(time())
        update_value = dict(task_status="%s" % task_status, user_name=user_name, reason_desc=reason_desc,
                            update_time=update_time)
        result = self.db.execute_update(self.scheduler_status, update_value, {"task_type": self.task_type})
        if result <=0:
            return self._new_task_status(task_status, user_name, reason_desc)
        return True, result

    def select_scheduler_status(self):
        cols = ["task_status", "user_name", "reason_desc", "update_time"]
        db_items = self.db.execute_select(self.scheduler_status, {"task_type": self.task_type}, cols=cols, package=True)
        if len(db_items) <= 0:
            info = {}
            for col in cols:
                info[col] = None
            return True, info
        return True, db_items[0]


class DayTaskManager(TaskManager):

    basic_time = datetime.strptime("2016-11-27 00:00:00", TIME_FORMAT)

    def __init__(self, task_type):
        super(DayTaskManager, self).__init__(task_type)
        pass

    @staticmethod
    def current_task_no():
        pass_time = datetime.now() - DayTaskManager.basic_time
        pass_days = int(pass_time.total_seconds() / 86400)
        return pass_days

    @staticmethod
    def task_no_2_str(task_no):
        return (DayTaskManager.basic_time + timedelta(hours=task_no)).strftime(TIME_FORMAT)

    def register_new_task(self, user_name, reason, reason_desc):
        return super(DayTaskManager, self).register_new_task(self.current_task_no(), user_name, reason, reason_desc)
#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
from datetime import datetime, timedelta
from time import time
sys.path.append("..")
from Tools.Mysql_db import DB
from Class import TIME_FORMAT
from Check import check_chinese_en, check_http_method, check_path, check_sql_character, check_char_num_underline, check_char, check_int

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class ReleaseManager:

    def __init__(self):
        self.db = DB()
        self.release_task = "release_task"
        self.basic_time = datetime.strptime("2016-09-02 11:27:11", TIME_FORMAT)

    def new_release_task(self, user_name, reason, reason_desc):
        release_time = datetime.now() - self.basic_time
        release_no = release_time.seconds / 3600 + release_time.days * 24
        status_info = "%s1" % int(time())
        args = dict(release_no=release_no, user_name=user_name, reason=reason, reason_desc=reason_desc,
                    status_info=status_info)
        result = self.db.execute_insert(self.release_task, args=args, ignore=True)
        if result <= 0:
            return False, u"任务已存在"
        return True, release_no

    def update_release_task(self, release_no, run_result=True):
        status_info = "|%s%s" % (int(time()), 1 if run_result is True else 0)
        update_sql = "UPDATE %s SET status_info=CONCAT(status_info, '%s') WHERE release_no=%s;" \
                     % (self.release_task, status_info, release_no)
        self.db.execute(update_sql)
        return True, "success"

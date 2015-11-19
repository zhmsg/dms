#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Class import table_manager, TIME_FORMAT
from Check import check_sql_character

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class BugManager:

    def __init__(self):
        self.db = DB()
        self.bug = table_manager.bug
        self.bug_owner = table_manager.bug_owner
        self.bug_example = table_manager.bug_example

    def new_bug_info(self, bug_title, submitter):
        submit_time = datetime.now().strftime(TIME_FORMAT)
        bug_no = uuid.uuid1().hex
        bug_title = check_sql_character(bug_title)[:50]
        insert_sql = "INSERT INTO %s (bug_no,bug_title,submitter,submit_time) VALUES ('%s','%s','%s','%s');" \
                     % (self.bug, bug_no, bug_title, submitter, submit_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"bug_no": bug_no, "bug_title": bug_title, "submitter": submitter, "submit_time": submit_time}

    def new_bug_link(self, bug_no, user_name, link_type):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        link_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (bug_no,user_name,type,link_time) VALUES ('%s','%s','%s','%s');" \
                     % (self.bug_owner, bug_no, user_name, link_type, link_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"bug_no": bug_no, "user_name": user_name, "link_type": link_type, "link_time": link_time}

    def new_bug_example(self, bug_no, example_type, content):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        add_time = datetime.now().strftime(TIME_FORMAT)
        content = check_sql_character(content)
        insert_sql = "INSERT INTO %s (bug_no,type,content,add_time) VALUES ('%s','%s','%s','%s');" \
                     % (self.bug_example, bug_no, example_type, content, add_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"bug_no": bug_no, "example_type": example_type, "content": content, "add_time": add_time}

    def update_bug_status(self, bug_no, status):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        update_sql = "UPDATE %s SET bug_status=%s WHERE bug_no='%s';" % (self.bug_example, status, bug_no)
        result = self.db.execute(update_sql)
        return True, result

# encoding: utf-8
# !/usr/bin/env python

import json
from datetime import date, datetime
import os
from Tools import env
from mysqldb_rich.db2 import RichDB


__author__ = 'zhouheng'


class DB(RichDB):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
    conn = None
    cursor = None
    _sock_file = ''

    def __init__(self, host="", mysql_user="dms", mysql_password="gene_ac252", mysql_db="dms", port=None):
        if env == "Development":
            self.host = "172.16.110.10"
            self.port = 3306
        elif env == "Production":
            self.host = "localhost"
            self.port = 9536
        else:
            self.host = "127.0.0.1"
            self.port = 9536
        if host != "":
            self.host = host
            self.port = 3306
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.db = mysql_db
        if port is not None:
            self.port = port
        self.url = "mysql://%s:%s@%s/%s" % (self.mysql_user, self.mysql_password, self.host, self.db)
        RichDB.__init__(self, self.host, self.port, self.mysql_user, self.mysql_password, self.db)

    def backup_table(self, t_name, sql_path, db=None):
        if db is None:
            db = self.db
        os.system("rm -rf %s" % sql_path)
        backup_cmd = "mysqldump -h%s -u%s -p%s --skip-lock-tables %s %s >> %s" % (self.host, self.mysql_user,
                                                                                  self.mysql_password, db, t_name,
                                                                                  sql_path)
        os.system(backup_cmd)


class DBItem(object):

    def __init__(self, t_name, **kwargs):
        self.t_name = t_name
        super(DBItem, self).__init__()
        self.db = kwargs.pop("db", None)
        if self.db is None:
            self.db = DB(**kwargs)

    def execute_select(self, where_value={"1": 1}, where_cond=None, cols=None, package=True, **kwargs):
        return self.db.execute_select(self.t_name, where_value=where_value, where_cond=where_cond, cols=cols,
                                      package=package, **kwargs)

    def fetchone(self):
        return self.db.fetchone()

    def fetchall(self):
        return self.db.fetchall()

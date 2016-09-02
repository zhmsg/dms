# encoding: utf-8
# !/usr/bin/env python

import MySQLdb
from Tools import env

__author__ = 'zhouheng'

"""
Usage:
    from Mysql_db import DB
     db = DB()
     db.execute(sql)
     db.fetchone()
     db.fetchall()
     :return same as MySQLdb
"""


remote_host = "127.0.0.1"
local_host = "127.0.0.1"


class DB(object):
    conn = None
    cursor = None
    _sock_file = ''

    def __init__(self, host="", mysql_user="dms", mysql_password="gene_ac252", mysql_db="dms"):
        if env == "Development":
            self.host = "192.168.120.10"
        elif env == "Production":
            self.host = "localhost"
        else:
            self.host = "10.25.244.32"
        if host != "":
            self.host = host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.db = mysql_db

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=3306, user=self.mysql_user,
                                    passwd=self.mysql_password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)

    def execute(self, sql_query, args=None, freq=0):
        if self.cursor is None:
            self.connect()
        try:
            handled_item = self.cursor.execute(sql_query, args=args)
        except MySQLdb.Error as error:
            print(error)
            if freq >= 5:
                raise Exception(error)
            self.connect()
            return self.execute(sql_query=sql_query, args=args, freq=freq+1)
        return handled_item

    def execute_select(self, table_name, where_value, cols=None):
        args = dict(where_value).values()
        if len(args) <= 0:
            return 0
        if cols is None:
            select_item = "*"
        else:
            select_item = ",".join(tuple(cols))
        sql_query = "SELECT * FROM %s WHERE %s=%%s;" \
                    % (select_item, table_name, "=%s AND ".join(dict(where_value).keys()))
        return self.execute(sql_query, args)

    def execute_insert(self, table_name, args, ignore=False):
        keys = dict(args).keys()
        if ignore is True:
            sql_query = "INSERT IGNORE INTO %s (%s) VALUES (%%(%s)s);" % (table_name, ",".join(keys), ")s,%(".join(keys))
        else:
            sql_query = "INSERT INTO %s (%s) VALUES (%%(%s)s);" % (table_name, ",".join(keys), ")s,%(".join(keys))
        return self.execute(sql_query, args=args)

    def execute_update(self, table_name, update_value, where_value):
        args = dict(update_value).values()
        if len(args) <= 0:
            return 0
        where_args = dict(where_value).values()
        args.extend(where_args)
        sql_query = "UPDATE %s SET %s=%%s WHERE %s=%%s;" % (table_name, "=%s,".join(dict(update_value).keys()), "=%s,".join(dict(where_value).keys()))
        return self.execute(sql_query, args=args)

    def execute_delete(self, table_name, where_value):
        args = dict(where_value).values()
        if len(args) <= 0:
            return 0
        sql_query = "DELETE FROM %s WHERE %s=%%s;" % (table_name, "=%s AND ".join(dict(where_value).keys()))
        return self.execute(sql_query, args)

    def fetchone(self):
        one_item = self.cursor.fetchone()
        return one_item

    def fetchall(self):
        all_item = self.cursor.fetchall()
        return all_item

    def close(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()

    def format_string(self, str):
        return MySQLdb.escape_string(str)

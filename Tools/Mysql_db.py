# encoding: utf-8
# !/usr/bin/env python

import MySQLdb

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


remote_host = "localhost"
local_host = "127.0.0.1"


class DB(object):
    conn = None
    cursor = None
    _sock_file = ''

    def __init__(self, local=False, host="", mysql_user="dms", mysql_password="gene_ac252", mysql_db="dms"):
        if local is True:
            self.host = local_host
        else:
            self.host = remote_host
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

    def execute(self, sql_query, freq=0):
        if self.cursor is None:
            self.connect()
        try:
            handled_item = self.cursor.execute(sql_query)
        except MySQLdb.Error as error:
            print(error)
            if freq >= 5:
                raise Exception(error)
            self.connect()
            return self.execute(sql_query=sql_query, freq=freq+1)
        return handled_item

    def fetchone(self):
        try:
            one_item = self.cursor.fetchone()
        except Exception, e:
            one_item = ()
        return one_item

    def fetchall(self):
        try:
            all_item = self.cursor.fetchall()
        except Exception, e:
            all_item = ()
        return all_item

    def close(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()

    def format_string(self, str):
        return MySQLdb.escape_string(str)

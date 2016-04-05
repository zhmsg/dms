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

    def create_table(self, table_name, table_desc, force=False, table_comment=""):
        try:
            show_sql = "SHOW TABLES LIKE '%s';" % table_name
            result = self.execute(show_sql)
            execute_message = ""
            if result == 1:
                if force:
                    del_sql = "DROP TABLE  %s;" % table_name
                    print(del_sql)
                    self.execute(del_sql)
                    execute_message += "Delete The Original Table %s \n" % table_name
                else:
                    return False, "%s Table Already Exists" % table_name
            create_table_sql = "CREATE TABLE %s (" % table_name
            primary_key = []
            for value in table_desc:
                create_table_sql += "%s %s" % (value[0], value[1])
                if value[2] == "NO":
                    create_table_sql += " NOT NULL"
                if value[3] == "PRI":
                    primary_key.append(value[0])
                    # create_table_sql += " PRIMARY KEY"
                if value[4] is not None and value[4] != "None":
                    create_table_sql += " default %s" % value[4]
                if value[5] != "":
                    create_table_sql += " %s" % value[5]

                if len(value) >= 7:
                    create_table_sql += " COMMENT '%s'" % value[6]
                create_table_sql += ","
            if primary_key != []:
                create_table_sql += " PRIMARY KEY (%s)," % ",".join(primary_key)
            if table_comment != "":
                create_table_sql = create_table_sql[:-1] + ") COMMENT '%s'  DEFAULT CHARSET=utf8;" % table_comment
            else:
                create_table_sql = create_table_sql[:-1] + ") DEFAULT CHARSET=utf8;"
            self.execute(create_table_sql)
            execute_message += "CREATE TABLE %s Success \n" % table_name
            return True, execute_message
        except Exception, e:
            error_message = str(e.args)
            print(create_table_sql)
            return False, "fail:%s." % error_message


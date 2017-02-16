# encoding: utf-8
# !/usr/bin/env python

import MySQLdb
import json
from datetime import date, datetime
import os
from Tools import env


__author__ = 'zhouheng'


class DB(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
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
        self.url = "mysql://%s:%s@%s/%s" % (self.mysql_user, self.mysql_password, self.host, self.db)

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=3306, user=self.mysql_user,
                                    passwd=self.mysql_password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)

    def literal(self, s):
        if not self.conn:
            self.connect()
        if isinstance(s, dict) or isinstance(s, tuple) or isinstance(s, list):
            s = json.dumps(s)
        return self.conn.literal(s)

    @staticmethod
    def merge_where(where_value=None, where_is_none=None, where_cond=None):
        args = []
        if where_cond is None:
            where_cond = list()
        else:
            where_cond = list(where_cond)
        if where_value is not None:
            where_args = dict(where_value).values()
            args.extend(where_args)
            for key in dict(where_value).keys():
                where_cond.append("%s=%%s" % key)
        if where_is_none is not None and len(where_is_none) > 0:
            for key in where_is_none:
                where_cond.append("%s is NULL" % key)
        return where_cond, args

    def execute(self, sql_query, args=None, freq=0):
        if self.cursor is None:
            self.connect()
        if args is not None:
            if isinstance(args, dict):
                sql_query = sql_query % dict((key, self.literal(item)) for key, item in args.iteritems())
            else:
                sql_query = sql_query % tuple([self.literal(item) for item in args])
        try:
            handled_item = self.cursor.execute(sql_query)
        except MySQLdb.Error as error:
            print(error)
            if freq >= 3 or error.args[0] in [1054, 1064, 1146]:  # 列不存在 sql错误 表不存在
                raise MySQLdb.Error(error)
            self.connect()
            return self.execute(sql_query=sql_query, freq=freq+1)
        return handled_item

    def execute_select(self, table_name, where_value={"1": 1}, where_cond=None, cols=None, package=True, **kwargs):
        where_is_none = kwargs.pop("where_is_none", None)
        where_cond, args = self.merge_where(where_value=where_value, where_cond=where_cond, where_is_none=where_is_none)
        if cols is None:
            select_item = "*"
        else:
            select_item = ",".join(tuple(cols))
        if len(where_cond) > 0:
            sql_query = "SELECT %s FROM %s WHERE %s" % (select_item, table_name, " AND ".join(where_cond))
        else:
            sql_query = "SELECT %s FROM %s" % (select_item, table_name)
        order_by = kwargs.pop("order_by", None)
        order_desc = kwargs.pop("order_desc", False)
        limit = kwargs.pop("limit", None)
        if order_by is not None and (isinstance(order_by, list) or isinstance(order_by, tuple)):
            sql_query += " ORDER BY %s" % ",".join(order_by)
            if order_desc is True:
                sql_query += " DESC"
        if isinstance(limit, int):
            sql_query += " LIMIT %s" % limit
        sql_query += ";"
        exec_result = self.execute(sql_query, args)
        if cols is not None and package is True:
            db_items = self.fetchall()
            select_items = []
            for db_item in db_items:
                r_item = dict()
                for i in range(len(cols)):
                    c_v = db_item[i]
                    if isinstance(c_v, datetime):
                        c_v = c_v.strftime(self.TIME_FORMAT)
                    elif isinstance(c_v, date):
                        c_v = c_v.strftime(self.DATE_FORMAT)
                    elif isinstance(c_v, str):
                        if c_v == "\x00":
                            c_v = False
                        elif c_v == "\x01":
                            c_v = True
                        else:
                            print(c_v)
                    r_item[cols[i]] = c_v
                select_items.append(r_item)
            return select_items
        return exec_result

    def execute_insert(self, table_name, args, ignore=False):
        keys = dict(args).keys()
        if ignore is True:
            sql_query = "INSERT IGNORE INTO %s (%s) VALUES (%%(%s)s);" % (table_name, ",".join(keys), ")s,%(".join(keys))
        else:
            sql_query = "INSERT INTO %s (%s) VALUES (%%(%s)s);" % (table_name, ",".join(keys), ")s,%(".join(keys))
        return self.execute(sql_query, args=args)

    def execute_update(self, table_name, update_value, where_value=None, where_is_none=[], where_cond=None):
        args = dict(update_value).values()
        if len(args) <= 0:
            return 0
        sql_query = "UPDATE %s SET %s=%%s WHERE " % (table_name, "=%s,".join(dict(update_value).keys()))
        if isinstance(where_cond, tuple) or isinstance(where_cond, list):
            where_cond = list(where_cond)
        else:
            where_cond = []
        if where_value is not None:
            where_args = dict(where_value).values()
            args.extend(where_args)
            for key in dict(where_value).keys():
                where_cond.append("%s=%%s" % key)
        if len(where_is_none) > 0:
            for key in where_is_none:
                where_cond.append("%s is NULL" % key)
        sql_query += " AND ".join(where_cond)
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

    def backup_table(self, t_name, sql_path, db=None):
        if db is None:
            db = self.db
        os.system("rm -rf %s" % sql_path)
        backup_cmd = "mysqldump -h%s -u%s -p%s --skip-lock-tables %s %s >> %s" % (self.host, self.mysql_user,
                                                                                  self.mysql_password, db, t_name,
                                                                                  sql_path)
        os.system(backup_cmd)

    def close(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()

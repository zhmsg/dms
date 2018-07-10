# encoding: utf-8
# !/usr/bin/env python

import MySQLdb
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

    def execute_select_left(self, b_t_name, j_t_name, join_key, **kwargs):
        where_is_none = kwargs.pop("where_is_none", None)
        where_value = kwargs.pop("where_value", {"1": 1})
        where_cond = kwargs.pop("where_cond", None)
        where_cond, args = self.merge_where(where_value=where_value, where_cond=where_cond, where_is_none=where_is_none)
        cols = list()
        package_keys = list()
        b_cols = kwargs.pop("b_cols", None)
        if b_cols is not None and isinstance(b_cols, list):
            for b_col in b_cols:
                cols.append("%s.%s" % (b_t_name, b_col))
                package_keys.append(b_col)
        j_cols = kwargs.pop("j_cols", None)
        if j_cols is not None and isinstance(j_cols, list):
            for j_col in j_cols:
                cols.append("%s.%s" % (j_t_name, j_col))
                package_keys.append(j_col)
        if len(cols) <= 0:
            s_item = "*"
        else:
            s_item = ",".join(cols)
        sql_query = "SELECT {0} FROM {1} LEFT JOIN {2} ON {1}.{3}={2}.{3}".format(s_item, b_t_name, j_t_name, join_key)
        if len(where_cond) > 0:
            sql_query += " WHERE %s" % " AND ".join(where_cond)
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
        if len(package_keys) > 0:
            db_items = self.fetchall()
            select_items = []
            for db_item in db_items:
                r_item = dict()
                for i in range(len(package_keys)):
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
                    r_item[package_keys[i]] = c_v
                select_items.append(r_item)
            return select_items
        return exec_result

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

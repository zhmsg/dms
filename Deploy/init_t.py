# !/usr/bin/env python
# coding: utf-8
import os
import sys

from mysqldb_rich.db2 import DB, TableDB

__author__ = 'meisa'

script_dir = os.path.dirname(__file__)

if __name__ == "__main__":
    db_conf_path = os.path.join(script_dir, "..", "mysql_app.conf")
    if len(sys.argv) >= 2:
        root_password = sys.argv[1]
    # else:
    #     root_password = "lcYH223&*"
        db = DB(conf_path=db_conf_path, user="root", password=root_password)
        db.root_init_conf('%')
    db2 = TableDB(conf_path=db_conf_path)
    db2.create_from_dir(os.path.join(script_dir, "..", "Table"))

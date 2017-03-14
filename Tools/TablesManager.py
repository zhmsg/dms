#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Tools.Mysql_db import DB


class TableManager(object):
    def __init__(self, *args, **kwargs):
        db = kwargs.pop("db", None)
        if db is not None and isinstance(db, DB):
            self.db = db
        else:
            conf_dir = kwargs.pop("conf_dir", None)
            readonly = kwargs.pop("readonly", False)
            if conf_dir is not None:
                self.db = DB()
            else:
                self.db = None
        self.t_name = kwargs.pop("t_name", None)

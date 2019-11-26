#! /usr/bin/env python
# coding: utf-8

from mysqldb_rich.db2 import DB

from dms.utils.database_config import MysqlConfig
from dms.utils.singleton import Singleton


class UnsetValue(Singleton):

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def is_unset(cls, value):
        return value == cls.get_instance()

    @classmethod
    def not_unset(cls, value):
        return not cls.is_unset(value)


class DBObject(object):
    db_config = MysqlConfig()
    table_file = None

    def __init__(self):
        self.db = DB(conf_path=self.db_config.config_path)


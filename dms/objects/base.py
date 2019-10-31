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


_UNSET = UnsetValue.get_instance()


class DBObject(object):
    db_config = MysqlConfig()
    table_file = None

    def __init__(self):
        self.db = DB(conf_path=self.db_config.config_path)


class ResourceManager(DBObject):

    NAME = _UNSET

    def get_name(self):
        if UnsetValue.is_unset(self.NAME):
            raise NotImplementedError("Extension object not define NAME")
        return self.NAME

    @property
    def name(self):
        return self.get_name()

    @classmethod
    def get_modules_desc(cls):
        """
        return modules desc, a list
        :return:

        """
        return []

    @staticmethod
    def support_view():
        return []

    def __getattribute__(self, item):
        return super(ResourceManager, self).__getattribute__(item)

#! /usr/bin/env python
# coding: utf-8

from functools import wraps
import inspect

import sys
import uuid

sys.path.insert(0, "D:/Project/mysqldb-rich")

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

    @staticmethod
    def require_verify_args():
        return dict()

    @staticmethod
    def gen_uuid():
        return uuid.uuid4().hex

    def __getattribute__(self, item):
        attr_value = super(ResourceManager, self).__getattribute__(item)

        if inspect.ismethod(attr_value):
            if attr_value.__name__.startswith("_"):
                return attr_value
            if attr_value.__name__ in ["require_verify_args"]:
                return attr_value

            sign_parameters = inspect.signature(attr_value).parameters
            full_args = []
            has_kw = False
            for key in sign_parameters.keys():
                k_kind = sign_parameters[key].kind.name
                if k_kind == inspect.Parameter.VAR_KEYWORD.name:
                    has_kw = True
                    continue
                if k_kind == inspect.Parameter.POSITIONAL_OR_KEYWORD.name:
                    full_args.append(key)
            rv_args = self.require_verify_args()
            verify_key = rv_args.keys() & set(full_args)
            if not verify_key and not has_kw:
                return attr_value
            _key_index = dict()
            for key in verify_key:
                _key_index[key] = full_args.index(key)

            @wraps(attr_value)
            def verify_args_func(*args, **kwargs):
                l_args = list(args)
                for _key, _index in _key_index.items():
                    if len(args) > _index:
                        l_args[_index] = rv_args[_key](args[_index])
                for _key, _value in kwargs.items():
                    if _key in rv_args:
                        kwargs[_key] = rv_args[_key](_value)
                return attr_value(*l_args, **kwargs)
            return verify_args_func
        return attr_value


class ResourceExample(ResourceManager):
    NAME = "resource_example"

    @classmethod
    def require_verify_args(cls):
        return dict(ss=int, s=cls.echo)

    def _echo(self, ss):
        print(ss)

    @classmethod
    def echo(cls, s):
        print(s)

    def echo_more(self, s, *args):
        print(s)
        print(args)

    def echo_keys(self, s, **kwargs):
        print(s)
        print(kwargs)

    def echo_composite(self, s, ss="ss_default", *args, **kwargs):
        print(s)
        assert isinstance(ss, int)
        print(ss)
        print(args)
        print(kwargs)


if __name__ == "__main__":
    re_man = ResourceExample()

    re_man.echo("hello")
    # re_man.echo_more("hello", "1+1")
    # re_man.echo_keys("hello", ss="45")
    # re_man.echo_composite("s_hello", "23", "other_hello", s_key="key_hello")
    # re_man._echo(ss="sss")

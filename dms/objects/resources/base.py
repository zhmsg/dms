#! /usr/bin/env python
# coding: utf-8
import abc
from functools import wraps
import inspect

import sys
import uuid

__author__ = 'zhouhenglc'

from dms.objects.base import DBObject
from dms.objects.base import UnsetValue
from dms.objects.web_config import WebConfig


_UNSET = UnsetValue.get_instance()


class ResourceManager(DBObject):

    NAME = _UNSET
    REQUIRED_CONFIG = None

    def get_name(self):
        if UnsetValue.is_unset(self.NAME):
            raise NotImplementedError("Extension object not define NAME")
        return self.NAME

    @property
    def name(self):
        return self.get_name()

    @classmethod
    def get_required_config(cls):
        if cls.REQUIRED_CONFIG:
            return cls.REQUIRED_CONFIG
        return []

    def _load_config(self):
        web_c = WebConfig.get_instance()
        loaded = dict()
        missing = []
        for config_key in self.get_required_config():
            v = web_c.get_key(config_key)
            if v:
                loaded[config_key] = v
            else:
                missing.append(config_key)
        _config = {'loaded': loaded, 'missing': missing}
        setattr(self, '_config', _config)

    @property
    def config(self):
        if not hasattr(self, "_config"):
            self._load_config()
        return self._config['loaded']

    @property
    def missing_config(self):
        if not hasattr(self, "_config"):
            self._load_config()
        return self._config['missing']

    @property
    def valid(self):
        if self.missing_config:
            return False
        return True

    @classmethod
    def get_modules_desc(cls):
        """
        return modules desc
        :return:

        """
        return dict()

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
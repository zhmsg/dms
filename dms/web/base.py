# !/usr/bin/env python
# coding: utf-8
from flask import Blueprint, g, Response, jsonify, redirect
from flask_login import login_required
import functools

from flask_helper.view import View as OView

from dms.utils.log import getLogger
from dms.utils.manager import Explorer

__author__ = 'zhouhenglc'


class RegisterData(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args)
        return cls._instance

    def __init__(self):
        self._dict = {}

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def set(self, key, value):
        self._dict[key] = value

    def set_default(self, key, default):
        if key not in self._dict:
            self._dict[key] = default

    def append(self, key, value):
        _values = self.get(key)
        if not _values:
            _values = []
        _values.append(value)
        self.set(key, _values)

    def update(self, key, **kwargs):
        _values = self.get(key)
        if not _values:
            _values = {}
        _values.update(**kwargs)
        self.set(key, _values)


REGISTER_DATA = RegisterData()


explorer = Explorer.get_instance()


class View(OView):

    def __init__(self, name, import_name, *args, **kwargs):
        self.auth_required = kwargs.pop('auth_required', True)
        self.required_resource = kwargs.pop('required_resource', [])
        super().__init__(name, import_name, *args, **kwargs)
        if self.auth_required:
            @self.before_request
            @login_required
            def before_request():
                print(explorer.missing_config)
                for rr in self.required_resource:
                    if rr in explorer.missing_config:
                        redirect_url = "/config?keys=%s" % \
                                       ",".join(explorer.missing_config[rr])
                        return redirect(redirect_url)

    def get_global_endpoint(self, endpoint=None, view_func=None):
        if endpoint:
            sub_endpoint = endpoint
        elif view_func:
            sub_endpoint = view_func.func_name
        else:
            return None
        g_endpoint = "%s.%s" % (self.name, sub_endpoint)
        return g_endpoint

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func:
            @functools.wraps(view_func)
            def inner(*args, **kwargs):
                r = view_func(*args, **kwargs)
                if isinstance(r, Response):
                    return r
                elif isinstance(r, bool):
                    return 'True' if r else 'False'
                elif isinstance(r, dict):
                    return jsonify(r)
                elif isinstance(r, list):
                    rs = []
                    for item in r:
                        if hasattr(item, 'to_dict'):
                            rs.append(item.to_dict())
                        else:
                            rs.append(item)
                    return jsonify(rs)
                elif hasattr(r, 'to_json'):
                    return r.to_json()
                elif hasattr(r, 'to_dict'):
                    return jsonify(r.to_dict())
                return r
            OView.add_url_rule(self, rule, endpoint, inner, **options)
        else:
            OView.add_url_rule(self, rule, endpoint, view_func, **options)

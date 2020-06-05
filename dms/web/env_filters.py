# !/usr/bin/env python
# coding: utf-8
from functools import partial
import time

from dms.utils.ip import IPManager

__author__ = 'zhouhenglc'


ip = IPManager()


class EnvFilter(object):

    def __init__(self, name, func, *req_keys):
        self.name = name
        self.func = func
        self.req_keys = req_keys

    @classmethod
    def from_func(cls, func, *req_keys):
        name = func.__name__
        o = cls(name, func, *req_keys)
        return o

    def get_func(self, **kwargs):
        if self.req_keys:
            n_kwargs = {}
            for k in self.req_keys:
                n_kwargs[k] = kwargs[k]
            return partial(self.func, **n_kwargs)
        else:
            return self.func


def unix_timestamp(t, style="time"):
    if isinstance(t, (int, float)):
        x = time.localtime(t)
        if style == "time":
            return time.strftime('%H:%M:%S', x)
        elif style == "month":
            return time.strftime('%Y%m', x)
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", x)
    return t


def bit_and(num1, num2):
    return num1 & num2


def ip_str(ip_v):
    if type(ip_v) == int:
        return ip.ip_value_str(ip_value=ip_v)
    return ip_v


def make_static_url(filename, static_prefix_url):
    return static_prefix_url + "/" + filename


def make_default_static_url(filename):
    return "/static/" + filename


def make_static_html(filename, static_prefix_url):
    if filename.startswith("http"):
        src = filename
        default_src = filename
    else:
        src = make_static_url(filename, static_prefix_url)
        default_src = make_default_static_url(filename)
    if filename.endswith(".js"):
        html_s = "<script type=\"text/javascript\" src=\"%s\" onerror=\"this.src='%s'\"></script>" % (src, default_src)
    else:
        html_s = "<link rel=\"stylesheet\" href=\"%s\" onerror=\"this.href='%s'\">" % (src, default_src)
    return html_s


__all__ = [EnvFilter.from_func(make_static_html, 'static_prefix_url'),
           EnvFilter.from_func(make_static_url, 'static_prefix_url'),
           ]
#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import time
from Class.IP import IPManager
from Config.Config import *

ip = IPManager()


def unix_timestamp(t, style="time"):
    if type(t) == int or type(t) == long:
        x = time.localtime(t)
        if style == "time":
            return time.strftime('%H:%M:%S', x)
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", x)
    return t


def bit_and(num1, num2):
    return num1 & num2


def ip_str(ip_v):
    if type(ip_v) == int or type(ip_v) == long:
        return ip.ip_value_str(ip_value=ip_v)
    return ip_v


def make_static_url(filename):
    return static_prefix_url + "/" + filename


def make_default_static_url(filename):
    return "/static/" + filename


def make_static_html(filename):
    src = make_static_url(filename)
    default_src = make_default_static_url(filename)
    if filename.endswith(".js"):
        html_s = "<script type=\"text/javascript\" src=\"%s\" onerror=\"this.src='%s'\"></script>" % (src, default_src)
    else:
        html_s = "<link rel=\"stylesheet\" href=\"%s\" onerror=\"this.href='%s'\">" % (src, default_src)
    return html_s

#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import time
import re
from Tools.MyIP import IPManager
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
    if filename.startswith("http"):
        src = filename
        default_src = filename
    else:
        src = make_static_url(filename)
        default_src = make_default_static_url(filename)
    if filename.endswith(".js"):
        html_s = "<script type=\"text/javascript\" src=\"%s\" onerror=\"this.src='%s'\"></script>" % (src, default_src)
    else:
        html_s = "<link rel=\"stylesheet\" href=\"%s\" onerror=\"this.href='%s'\">" % (src, default_src)
    return html_s

trust_proxy = ["127.0.0.1", "10.25.244.32", "10.44.147.192"]
accept_agent = "(firefox|chrome|safari|window|GitHub|jyrequests|micro)"


def normal_request_detection(request_headers, remote_ip):
    x_forwarded_for = request_headers.get("X-Forwarded-For")
    real_ip_s = remote_ip
    if x_forwarded_for is not None:
        if remote_ip in trust_proxy:
            real_ip_s = x_forwarded_for.split(",")[0]
    real_ip = ip.ip_value_str(ip_str=real_ip_s)
    if real_ip <= 0:
        return False, u"IP受限"
    if "User-Agent" not in request_headers:
        return False, u"请使用浏览器访问"
    user_agent = request_headers["User-Agent"]
    if re.search(accept_agent, user_agent, re.I) is None:
        return False, u"浏览器版本过低"
    return True, [real_ip_s, real_ip]
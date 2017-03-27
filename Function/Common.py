#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import time
import base64
import re
import requests
import M2Crypto
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
accept_agent = "(firefox|chrome|safari|window|GitHub|jyrequests|micro|Aliyun)"


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


def verify_sign_str(pem_path, sign_str, authorization):
    resp = requests.get(pem_path)
    pub_key = M2Crypto.X509.load_cert_string(resp.text).get_pubkey()
    pub_key.reset_context("sha1")
    pub_key.verify_init()
    if isinstance(sign_str, unicode):
        sign_str = sign_str.encode("utf-8")
    pub_key.verify_update(sign_str)
    if isinstance(authorization, unicode):
        authorization = authorization.encode("utf-8")
    return pub_key.verify_final(authorization)


def verify_mns_message(request_method, x_headers, resource):
    content_md5 = x_headers.get("Content-Md5", None)
    content_type = x_headers.get("Content-Type", None).lower()
    request_time = x_headers.get("Date")
    cert_url = base64.b64decode(x_headers["X-Mns-Signing-Cert-Url"])

    if re.match("https://mnstest.[^/]+?.aliyuncs.com/", cert_url) is None:
        return 0
    if content_md5 is None:
        content_md5 = ""
    if content_type is None:
        content_type = ""
    x_headers_s = ""

    if x_headers is not None:
        if type(x_headers) == unicode:
            x_headers_s = x_headers
        else:
            for key in sorted(x_headers.keys()):
                if key.lower().startswith("x-mns"):
                    x_headers_s += key.lower() + ":" + x_headers[key] + "\n"
    sign_str = "%s\n%s\n%s\n%s\n%s%s" % (request_method, content_md5, content_type, request_time, x_headers_s, resource)
    sign_str = unicode(sign_str)
    authorization = base64.b64decode(x_headers["Authorization"])
    verify_r = verify_sign_str(cert_url, sign_str, authorization)
    return verify_r


if __name__ == "__main__":
    with open("/home/msg/Desktop/test_ouput.py", "r") as r:
        content = r.read()
        headers = dict()
        for item in content.split("\n"):
            if len(item) <= 1:
                continue
            key_value = item.split(":", 1)
            headers[key_value[0]] = key_value[1].strip()
        print verify_mns_message("POST", headers, "/message/receive")

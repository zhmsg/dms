#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os
import ConfigParser

if os.path.exists("../env.conf") is False:
    current_env = "Development"

else:
    with open("../env.conf") as r_env:
        current_env = r_env.read().strip()

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

redis_host = config.get(current_env, "redis_host")
static_prefix_url = config.get(current_env, "static_prefix_url")
company_ip_start = config.getint(current_env, "company_ip_start")
company_ip_end = config.getint(current_env, "company_ip_end")
company_ips = [company_ip_start, company_ip_end]
cookie_domain = config.get(current_env, "cookie_domain")
session_id_prefix = config.get(current_env, "session_id_prefix")
session_cookie_name = config.get(current_env, "session_cookie_name")

user_blacklist = []
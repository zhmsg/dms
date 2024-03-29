#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os
import configparser


script_dir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.abspath(os.path.join(script_dir, '..', 'env.conf'))
cfg_path = os.path.abspath(os.path.join(script_dir, '..', 'config.conf'))

if os.path.exists(env_path) is False:
    current_env = "Development"

else:
    with open(env_path) as r_env:
        current_env = r_env.read().strip()

# read config
config = configparser.ConfigParser()
config.read(cfg_path)

redis_host = config.get(current_env, "redis_host")
redis_port = config.get(current_env, "redis_port")
static_prefix_url = config.get(current_env, "static_prefix_url")
company_ip_start = config.getint(current_env, "company_ip_start")
company_ip_end = config.getint(current_env, "company_ip_end")
company_ips = [company_ip_start, company_ip_end]
cookie_domain = config.get(current_env, "cookie_domain")
session_id_prefix = config.get(current_env, "session_id_prefix")
session_cookie_name = config.get(current_env, "session_cookie_name")
web_prefix_url = config.get(current_env, "web_prefix_url")
request_special_protocol = config.get(current_env, "request_special_protocol").split(",")
task_log_url = config.get(current_env, "task_log_url")

sx_variant = config.get(current_env, "sx_variant")
check_variant = [False]

conf_dir = config.get(current_env, "conf_dir")

user_blacklist = []
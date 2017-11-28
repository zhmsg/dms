#! /usr/bin/env python
# coding: utf-8

import os
import ConfigParser
from JYAliYun.AliYunAccount import RAMAccount
from JYAliYun.AliYunMNS.AliMNSServer import MNSServerManager

__author__ = 'ZhouHeng'

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT_STR = "%Y%m%d%H%M%S"
DATE_FORMAT_STR = "%Y%m%d"


if os.path.exists("../env.conf") is False:
    env = "Development"
else:
    with open("../env.conf") as r_env:
        env = r_env.read().strip()

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

wx_service = config.get(env, "wx_service")
release_host = config.get(env, "release_host")
release_dir = config.get(env, "release_dir")
release_host_port = config.getint(env, "release_host_port")
jd_mysql_host = config.get(env, "jd_mysql_host")
jd_mysql_db = config.get(env, "jd_mysql_db")
dyups_server = config.get(env, "dyups_server")
sample_service = config.get(env, "sample_service")
right_service = config.get(env, "right_service")
conf_dir = config.get(env, "conf_dir")
mongo_host = config.get(env, "mongo_host")

mns_account = RAMAccount(conf_dir=conf_dir, conf_name="mns.conf")
mns_server = MNSServerManager(ram_account=mns_account, conf_dir=conf_dir)

topic_name = "JYWaring"
mns_topic = mns_server.get_topic(topic_name)

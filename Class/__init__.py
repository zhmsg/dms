#! /usr/bin/env python
# coding: utf-8

import os
import ConfigParser

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
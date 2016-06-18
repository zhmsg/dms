#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os

if os.path.exists("../env.conf") is False:
    env = "Development"
else:
    with open("../env.conf") as r_env:
        env = r_env.read()

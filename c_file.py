#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os

current_dir = os.getcwd()

class_dir = current_dir + "/Class"

for class_file in os.listdir(class_dir):
    if class_file.endswith(".py"):
        file_name = class_dir + "/" + class_file[:-3]
        os.system("sh build_c.sh %s" % file_name)

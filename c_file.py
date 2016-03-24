#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os

read = open("env.conf")
content = read.read()
read.close()
if content == "Development":
    build_cmd = "g++ -fPIC $1.c -o $1.so -shared -I/usr/include/python2.7 -I/usr/lib/python2.7/config"
else:
    build_cmd = "g++ -fPIC $1.c -o $1.so -shared -I/home/msg/dmsenv/include/python2.7 -I/home/msg/dmsenv/lib/python2.7/config"
write = open("build_c.sh", "w")
write.write("cython $1.py\n")
write.write("%s\n" % build_cmd)
write.write("rm -rf $1.py\n")
write.write("rm -rf $1.c")
write.close()

current_dir = os.getcwd()

class_dir = current_dir + "/Class"

for class_file in os.listdir(class_dir):
    if class_file.endswith(".py") and class_file != "develop_table.py":
        file_name = class_dir + "/" + class_file[:-3]
        os.system("sh build_c.sh %s" % file_name)

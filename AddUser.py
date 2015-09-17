#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Class.User import UserManager
from Tools.MyEmail import MyEmailManager

user_m = UserManager()
my_email = MyEmailManager()

user_info = []
user_info.append({"user_name": "wangfei", "password": "wangfei@gene.ac", "role": "market"})
user_info.append({"user_name": "zhaoguoguang", "password": "zhaoguoguang@gene.ac", "role": "market"})

user_info.append({"user_name": "zhaolianhe", "password": "zhaolianhe@gene.ac", "role": "upload"})

user_info.append({"user_name": "yangrui", "password": "yangrui@gene.ac", "role": "calc"})

user_info.append({"user_name": "budechao", "password": "budechao@gene.ac", "role": "sys"})

for user in user_info:
    result, message = user_m.new(user["user_name"], user["password"], user["role"])
    if result is False:
        print(message)
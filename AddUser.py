#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Class.User import UserManager
from Tools.MyEmail import MyEmailManager

user_m = UserManager()
my_email = MyEmailManager()

user_info = []
user_info.append({"user_name": "wangfei", "password": "wangfei@gene.ac", "role": 1})
user_info.append({"user_name": "zhaoguoguang", "password": "zhaoguoguang@gene.ac", "role": 1})

user_info.append({"user_name": "zhaolianhe", "password": "zhaolianhe@gene.ac", "role": 2})

user_info.append({"user_name": "yangrui", "password": "yangrui@gene.ac", "role": 4})

user_info.append({"user_name": "budechao", "password": "budechao@gene.ac", "role": 7})

for user in user_info:
    result, message = user_m.new(user["user_name"], user["password"], user["role"])
    if result is False:
        print(message)
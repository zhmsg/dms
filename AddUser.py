#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Class.User import UserManager

user_m = UserManager()

user_info = []
user_info.append({"user_name": "wangfei", "password": "wangfei@gene.ac", "role": "market"})
user_info.append({"user_name": "zhaoguoguang", "password": "zhaoguoguang@gene.ac", "role": "market"})

user_info.append({"user_name": "zhaolianhe", "password": "zhaolianhe@gene.ac", "role": "upload"})

user_info.append({"user_name": "yangrui", "password": "yangrui@gene.ac", "role": "calc"})

for user in user_info:
    result, message = user_m.new(user["user_name"], user["password"], user["role"])
    if result is False:
        print(message)
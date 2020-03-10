#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
from functools import wraps
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue


from dms.objects.user import UserObject
from dms.utils.manager import Explorer

resources_m = Explorer.get_instance()
ur_man = resources_m.get_object_manager("user_role")
user_m = UserObject()

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = '/user/policies'



user_role_view = create_blue('user_role_view', url_prefix=url_prefix,
                               required_resource=[ur_man])


@user_role_view.route("", methods=["GET"])
def mine_policies():
    policies = ur_man.get_policies(g.user_name)
    data = {'role': g.user_role, 'policies': policies}
    return jsonify({'status': True, 'data': data})


@user_role_view.route("/manager", methods=["GET"])
def manager_policies():
    is_admin = user_m.is_admin(g.user_role)
    if not is_admin:
        policies = ur_man.get_policies(g.user_name)
        man_pms = resources_m.manager_modules(policies)
        man_modules = dict()
        for m_name in man_pms:
            if m_name in resources_m.modules:
                man_modules[m_name]= resources_m.m[m_name]
    else:
        man_modules = resources_m.modules
    return jsonify({'status': True, 'data': man_modules})


@user_role_view.route("/other", methods=["POST"])
def other_user_role():
    data = request.json
    other_user = data['user_name']
    is_admin = user_m.is_admin(g.user_role)
    # 获取其他用户角色
    other_role = user_m.get_user_role(other_user)
    if other_role is None:
        return jsonify({'status': False, 'data': '用户不存在'})
    if other_role >= g.user_role:
        # 其他用户角色必须小于当前用户
        return jsonify({'status': False, 'data': 'forbidden'})

    # 获取其他用户拥有的权限
    other_policies = ur_man.get_policies(other_user)

    # 只返回当前用户管理的模块 其他用户的权限
    part_policies = {}
    if not is_admin:
        # 获取当前用户管理的模块
        mine_policies = ur_man.get_policies(g.user_name)
        man_modules = resources_m.manager_modules(mine_policies)

        for m_name in man_modules:
            if m_name in other_policies:
                part_policies[m_name] = other_policies[m_name]
            else:
                part_policies[m_name] = []
    else:
        part_policies = other_policies
    data = {'role': g.user_role, 'policies': part_policies}
    return jsonify({'status': True, 'data': data})

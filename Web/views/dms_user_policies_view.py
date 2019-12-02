#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
from functools import wraps
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue


from dms.utils.manager import ResourcesManager


ur_man = ResourcesManager.get_instance().get_object_manager("user_role")

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = '/user/policies'



user_role_view = create_blue('user_role_view', url_prefix=url_prefix,
                               required_resource=[ur_man])

@user_role_view.route("", methods=["GET"])
def mine_role():
    policies = ur_man.get_policies(g.user_name)
    data = {'role': g.user_role, 'policies': policies}
    return jsonify({'status': True, 'data': data})

#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import request, jsonify, g



from dms.objects.user import UserObject
from dms.objects.web_config import WebConfig

from Tools.RenderTemplate import RenderTemplate

from Web import config_url_prefix
from Web import create_blue


url_prefix = config_url_prefix
rt = RenderTemplate("Web_Config", url_prefix=url_prefix)

__author__ = 'Zhouheng'


config_man = WebConfig.get_instance()
user_man = UserObject()
config_view = create_blue('dms_config_view', url_prefix=url_prefix, auth_required=True)


@config_view.route('', methods=['GET'])
def config_page():
    return rt.render('config.html')

@config_view.route('/values', methods=['GET'])
def get_config_value():
    if not user_man.is_admin(g.user_role):
        return jsonify({"status": False, "data": "无权限"})
    keys = request.args.get('keys', "").split(",")

    configs = config_man.get_keys(keys)
    return jsonify({'status': True, 'data': configs})


@config_view.route('/values', methods=['POST'])
def post_config_value():
    if not user_man.is_admin(g.user_role):
        return jsonify({"status": False, "data": "无权限"})
    request_data = request.json
    config_man.new_configs(request_data)
    return jsonify({"status": True, "data": True})

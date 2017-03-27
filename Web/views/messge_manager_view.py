#! /usr/bin/env python
# coding: utf-8

import os
import base64
from time import time
from random import randint
from datetime import datetime
from flask import request, send_from_directory, g, jsonify
from Tools.RenderTemplate import RenderTemplate
from Web import message_url_prefix as url_prefix, create_blue, verify_mns_message

__author__ = 'ZhouHeng'

rt = RenderTemplate("message", url_prefix=url_prefix)
message_view = create_blue('message_view', url_prefix=url_prefix, auth_required=False)


@message_view.route("/receive", methods=["POST"])
def receive_message_func():
    verify_r = verify_mns_message(request.method, request.headers, request.path)
    if verify_r != 1:
        return jsonify({"success": True, "data": "not save"})
    print(request.json)
    return jsonify({"success": True, "data": "success"})

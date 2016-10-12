#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from flask import render_template, request, redirect, jsonify, g
from flask_login import current_user

from Web import chat_url_prefix as url_prefix, create_blue, control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Chat"

chat_view = create_blue('chat_view', url_prefix=url_prefix)


@chat_view.route("/", methods=["GET"])
def show_param_info_func():
    return render_template("%s/Index.html" % html_dir)

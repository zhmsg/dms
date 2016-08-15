#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from flask import render_template, request, redirect
from flask_login import current_user

from Web import param_url_prefix as url_prefix, create_blue
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Param"

develop_param_view = create_blue('develop_param_view', url_prefix=url_prefix)


@develop_param_view.route("/", methods=["GET"])
def show_param_info_func():
    return render_template("%s/Param_Info.html" % html_dir)
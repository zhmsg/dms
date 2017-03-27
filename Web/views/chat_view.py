#!/user/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Zhouheng'

import sys
from flask import render_template

from Web import chat_url_prefix as url_prefix, create_blue

sys.path.append('..')

html_dir = "/Chat"

chat_view = create_blue('chat_view', url_prefix=url_prefix)


@chat_view.route("/", methods=["GET"])
def show_param_info_func():
    return render_template("%s/Index.html" % html_dir)

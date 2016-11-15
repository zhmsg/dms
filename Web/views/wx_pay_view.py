#! /usr/bin/env python
# coding: utf-8
import sys

from Tools.RenderTemplate import RenderTemplate
from Web import pay_url_prefix as url_prefix, create_blue

sys.path.append('..')

__author__ = 'Zhouheng'


rt = RenderTemplate("Pay", url_prefix=url_prefix)
pay_view = create_blue('pay_view', url_prefix=url_prefix, auth_required=False)


@pay_view.route("/", methods=["GET"])
def show_param_info_func():
    return rt.render("index.html")
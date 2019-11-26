#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from flask import request, render_template, redirect, session, url_for, jsonify, g, make_response, current_app
from flask.sessions import SecureCookieSessionInterface
from flask_login import login_user, current_user, logout_user
from flask_login import login_required
from werkzeug.security import gen_salt
from Class import mongo_host
from Class.User import RoleManager
from Web import User

from Tools.RenderTemplate import RenderTemplate

from Web import config_url_prefix
from Web import create_blue


url_prefix = config_url_prefix
rt = RenderTemplate("Web_Config", url_prefix=url_prefix)

__author__ = 'Zhouheng'



config_view = create_blue('dms_config_view', url_prefix=url_prefix, auth_required=True)


@config_view.route('', methods=['GET'])
def config_page():
    return rt.render('config.html')

@config_view.route('/', methods=['GET'])
def get_config_value():
    pass

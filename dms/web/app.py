import importlib
import signal

from flask import Blueprint, Flask, session

from flask_helper import Flask2

from dms.web.error_hander import handle_500
from dms.exceptions import DmsException
from dms.utils.log import getLogger

# TODO
from Web import *


__author__ = 'zhouhenglc'

LOG = getLogger()


def handle_signal(signal_num, frame):
    pass
    # async_worker = get_async_worker()
    # async_worker.catch_signal(signal_num)


def register_signal():
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    try:
        signal.signal(signal.SIGUSR1, handle_signal)
        signal.signal(signal.SIGUSR2, handle_signal)
        signal.signal(signal.SIGHUP, handle_signal)
    except AttributeError:
        pass


class User(UserMixin):
    user_name = ""

    def get_id(self):
        return self.user_name


login_manager = LoginManager()
# login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_name):
    user = User()
    user.user_name = user_name
    if "policies" not in session:
        session["policies"] = dict()
    user.policies = session["policies"]
    if "role" not in session:
        session["role"] = 0
    user.role = session["role"]
    return user


login_manager.login_view = "dms_bp.index"


def get_application():
    app = Flask2(__name__, log=LOG)
    app.secret_key = 'dms'
    app.cross_domain()
    login_manager.init_app(app)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(DmsException, handle_500)

    env = app.jinja_env

    env.globals["current_env"] = current_env
    env.globals["menu_url"] = dms_url_prefix + "/portal/"  # TODO
    env.globals["short_link_url"] = short_link_prefix

    env_filters = importlib.import_module('dms.web.env_filters').__all__
    _kwargs = {'static_prefix_url': '/static'}  # TODO
    for e_filter in env_filters:
        env.filters[e_filter.name] = e_filter.get_func(**_kwargs)

    env.variable_start_string = "{{ "
    env.variable_end_string = " }}"

    register_signal()
    return app

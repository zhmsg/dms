import importlib
import signal

from flask import Blueprint, Flask, session
from flask_login import LoginManager, UserMixin, login_required

from dms.web.error_hander import handle_500
from dms.exceptions import DmsException



__author__ = 'zhouhenglc'


def is_blueprint(obj):
    return isinstance(obj, Blueprint)


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
    app = Flask(__name__)
    app.secret_key = 'dms'
    login_manager.init_app(app)
    view_mod = importlib.import_module('dms.web.views')
    bps = view_mod.__all__
    for bp in bps:
        app.register_blueprint(bp)
    hook_mod = importlib.import_module('dms.web.hooks')
    hooks = hook_mod.__all__
    hooks.sort(key=lambda x: x.priority)
    app.before_request_funcs.setdefault(None, [])
    app.after_request_funcs.setdefault(None, [])
    for hook in hooks:
        h_obj = hook(app)
        app.before_request_funcs[None].append(h_obj.before_request)
        app.after_request_funcs[None].append(h_obj.after_request)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(DmsException, handle_500)
    register_signal()
    return app

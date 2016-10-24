# encoding: utf-8
# !/usr/bin/python

__author__ = 'zhouheng'
import ConfigParser
import tornado.web
from Web2.redis_session import RedisSessionInterface
from Class.Control import ControlManager
from Class.User import UserManager

http_handlers = []

control = ControlManager()
user_m = UserManager()
ado_prefix = "/tornado"

api_url_prefix = ado_prefix + "/dev/api"
status_url_prefix = ado_prefix + "/dev/api/status"
test_url_prefix = ado_prefix + "/dev/api/test"
bug_url_prefix = ado_prefix + "/dev/bug"
right_url_prefix = ado_prefix + "/dev/right"
param_url_prefix = ado_prefix + "/dev/param"
dev_url_prefix = ado_prefix + "/dev"
dms_url_prefix = ado_prefix + ""
data_url_prefix = ado_prefix + "/data"
log_url_prefix = ado_prefix + "/log"
tools_url_prefix = ado_prefix + "/tools"
release_url_prefix = ado_prefix + "/dev/release"
github_url_prefix = ado_prefix + "/github"
chat_url_prefix = ado_prefix + "/chat"

import os

if os.path.exists("../env.conf") is False:
    current_env = "Development"

else:
    with open("../env.conf") as r_env:
        current_env = r_env.read().strip()

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

redis_host = config.get(current_env, "redis_host")
static_prefix_url = config.get(current_env, "static_prefix_url")
company_ip_start = config.getint(current_env, "company_ip_start")
company_ip_end = config.getint(current_env, "company_ip_end")
company_ips = [company_ip_start, company_ip_end]
cookie_domain = config.get(current_env, "cookie_domain")
session_id_prefix = config.get(current_env, "session_id_prefix")
session_cookie_name = config.get(current_env, "session_cookie_name")

def make_static_url(filename):
    return "/static" + "/" + filename


def make_default_static_url(filename):
    return "/static/" + filename


def make_static_html(filename):
    src = make_static_url(filename)
    default_src= make_default_static_url(filename)
    if filename.endswith(".js"):
        html_s = "<script type=\"text/javascript\" src=\"%s\" onerror=\"this.src='%s'\"></script>" % (src, default_src)
    else:
        html_s = "<link rel=\"stylesheet\" href=\"%s\" onerror=\"this.href='%s'\">" % (src, default_src)
    return html_s


class GlobalInfo(object):

    def __init__(self):
        self.user_name = None
        self.user_role = 0


session_interface = RedisSessionInterface(redis_host, session_id_prefix, cookie_domain, session_cookie_name)


class BaseHandler(tornado.web.RequestHandler):
    route_url = ado_prefix

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.kwargs = {"current_env": "Tornado " + current_env, "g": GlobalInfo(), "role_value": user_m.role_value}
        self.session = session_interface.open_session(self)
        if "user_role" in self.session:
            self.kwargs["g"].user_role = self.session["user_role"]
        if "user_name" in self.session:
            self.kwargs["g"].user_name = self.session["user_name"]

    def data_received(self, chunk):
        pass

    def current_user(self):
        if "user_name" in self.session and "user_role" in self.session:
            return self.session["user_name"]

    def render(self, template_name, **kwargs):
        for key, value in kwargs.items():
            self.kwargs[key] = value
        super(BaseHandler, self).render(template_name, **self.kwargs)

    def get_current_user(self):
        session_id = self.get_cookie("jydms")

    def save_session(self):
        session_interface.save_session(self)

    def on_finish(self):
        pass

    def finish(self, chunk=None):
        session_interface.save_session(self)
        super(BaseHandler, self).finish(chunk)


class BaseAuthHandler(BaseHandler):
    route_url = BaseHandler.route_url

    def prepare(self):
        super(BaseAuthHandler, self).prepare()
        if "user_name" not in self.session or "user_role" not in self.session:
            self.redirect(dms_url_prefix + "/login/")


class ErrorHandler(tornado.web.RequestHandler):
    def initialize(self, status_code):
        self.set_status(status_code)

    @tornado.web.addslash
    def prepare(self):
        if self._status_code == 404:
            if self.request.uri.startswith(ado_prefix):
                self.redirect(self.request.uri[len(ado_prefix):])
            else:
                self.write("Not Found")
            return



# encoding: utf-8
# !/usr/bin/python

__author__ = 'zhouheng'
import json
import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from Web2.redis_session import RedisSessionInterface
from Class.Control import ControlManager
from Class.User import UserManager
from Function.Common import *

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


class GlobalInfo(object):
    def __init__(self):
        self.user_name = None
        self.user_role = 0


class TemplateRendering(object):

    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(self.settings['template_path'])
        env = Environment(loader=FileSystemLoader(template_dirs))
        env.globals["current_env"] = current_env
        env.globals["role_value"] = control.role_value
        env.filters['unix_timestamp'] = unix_timestamp
        env.filters['bit_and'] = bit_and
        env.filters['ip_str'] = ip_str
        env.filters['make_static_url'] = make_static_url
        env.filters['make_default_static_url'] = make_default_static_url
        env.filters['make_static_html'] = make_static_html
        env.filters['tojson'] = json.dumps
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


session_interface = RedisSessionInterface(redis_host, session_id_prefix, cookie_domain, session_cookie_name)


class BaseHandler(tornado.web.RequestHandler, TemplateRendering):
    route_url = ado_prefix

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.g = GlobalInfo()
        self.session = session_interface.open_session(self)
        if "user_role" in self.session:
            self.g.user_role = self.session["user_role"]
        if "user_name" in self.session:
            self.g.user_name = self.session["user_name"]
        menu_url = dms_url_prefix + "/portal/"
        self.kwargs = {"current_env": "Tornado " + current_env, "g": self.g, "role_value": user_m.role_value,
                       "menu_url": menu_url}
        self.request.args = {}
        for key, value in dict(self.request.arguments).items():
            self.request.args[key] = value[0]

    def data_received(self, chunk):
        pass

    def current_user(self):
        if "user_name" in self.session and "user_role" in self.session:
            return self.session["user_name"]

    def render(self, template_name, **kwargs):
        for key, value in kwargs.items():
            self.kwargs[key] = value
        super(BaseHandler, self).render(template_name, **self.kwargs)

    def render_template(self, template_name, **kwargs):
        for key, value in kwargs.items():
            self.kwargs[key] = value
        self.kwargs.update({
            'settings': self.settings,
            'request': self.request,
            'current_user': self.current_user,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html
        })
        content = super(BaseHandler, self).render_template(template_name, **self.kwargs)
        self.write(content)

    def get_current_user(self):
        pass

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
            self.redirect(dms_url_prefix + "/login/?next=" + self.request.path)


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

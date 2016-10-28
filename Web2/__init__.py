# encoding: utf-8
# !/usr/bin/python

__author__ = 'zhouheng'

from hashlib import sha512
from urllib import urlencode
import tornado.web
import tornado.escape
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
        env.globals["current_env"] = "Tornado " + current_env
        env.globals["role_value"] = control.role_value
        env.globals["menu_url"] = dms_url_prefix + "/portal/"
        env.filters['unix_timestamp'] = unix_timestamp
        env.filters['bit_and'] = bit_and
        env.filters['ip_str'] = ip_str
        env.filters['make_static_url'] = make_static_url
        env.filters['make_default_static_url'] = make_default_static_url
        env.filters['make_static_html'] = make_static_html
        env.filters['tojson'] = tornado.escape.json_encode
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


session_interface = RedisSessionInterface(redis_host, session_id_prefix, cookie_domain, session_cookie_name)


class BaseHandler(tornado.web.RequestHandler, TemplateRendering):
    url_prefix = ado_prefix
    route_url = ado_prefix + "/"
    html_dir = ""

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.g = GlobalInfo()
        self.session = session_interface.open_session(self)
        self.kwargs = {"g": self.g, "url_prefix": self.url_prefix}
        self.request.args = {}
        self.request.form = {}
        self.request.json = {}

    def data_received(self, chunk):
        pass

    def prepare(self):
        test_r, info = normal_request_detection(self.request.headers, self.request.remote_ip)
        if test_r is False:
            self.set_status(403)
            self.write(info)
            return self.finish()
        for key, value in dict(self.request.query_arguments).items():
            self.request.args[key] = value[0]
        for key, value in dict(self.request.body_arguments).items():
            self.request.form[key] = value[0].decode("utf-8")
        content_type = self.request.headers.get("Content-Type")
        if content_type == "application/json":
            if len(self.request.body) > 0:
                self.request.json = tornado.escape.json_decode(self.request.body)

    def get_session_id(self):
        user_agent = self.request.headers.get('User-Agent')
        if "User-Agent" in self.request.headers:
            user_agent = user_agent.encode('utf-8')
        address = self.request.headers.get('X-Forwarded-For', self.request.remote_ip)
        if address is not None:
            address = address.encode('utf-8').split(b',')[0].strip()
        base = '{0}|{1}'.format(address, user_agent)
        if str is bytes:
            base = unicode(base, 'utf-8', errors='replace')
        h = sha512()
        h.update(base.encode('utf8'))
        return h.hexdigest()

    @property
    def is_authenticated(self):
        if "user_id" not in self.session or "role" not in self.session or "_id" not in self.session:
            return False
        if self.session["_id"] != self.get_session_id():
            return False
        return True

    def get_current_user(self):
        if self.is_authenticated is True:
            return self.session["user_id"]
        return None

    def login_user(self, user_name, user_role):
        self.session["user_id"] = user_name
        self.session["role"] = user_role
        self.session["_id"] = self.get_session_id()

    def logout_user(self):
        if 'user_id' in self.session:
            self.session.pop('user_id')
        if '_fresh' in self.session:
            self.session.pop('_fresh')

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
        if self.html_dir != "":
            template_name = "%s/%s" % (self.html_dir, template_name)
        content = super(BaseHandler, self).render_template(template_name, **self.kwargs)
        self.write(content)

    def jsonify(self, return_obj):
        self.set_header("Content-Type", "application/json")
        self.write(tornado.escape.json_encode(return_obj))

    def write_error(self, status_code, **kwargs):
        res = str(status_code)
        if status_code == 500:
            res = "Error"
            if "exc_info" in kwargs:
                exc_info = kwargs["exc_info"]
                if len(exc_info) > 2:
                    res = str(exc_info[1])
        return self.write(res)

    def finish(self, chunk=None):
        session_interface.save_session(self)
        super(BaseHandler, self).finish(chunk)

    def on_finish(self):
        pass


class BaseAuthHandler(BaseHandler):
    route_url = BaseHandler.route_url

    def prepare(self):
        super(BaseAuthHandler, self).prepare()
        if not self.is_authenticated:
            next_url = self.request.uri
            login_url = dms_url_prefix + "/login/?"
            login_url += urlencode(dict(next=next_url))
            return self.redirect(login_url)
        self.g.user_role = self.session["role"]
        self.g.user_name = self.session["user_id"]


class ErrorHandler(tornado.web.RequestHandler):
    def initialize(self, status_code):
        self.set_status(status_code)

    @tornado.web.addslash
    def prepare(self):
        if self._status_code == 404:
            if self.request.uri.startswith(ado_prefix):
                return self.redirect(self.request.uri[len(ado_prefix):])
            else:
                return self.write("Not Found")
        return


class PingHandler(BaseHandler):
    route_url = BaseHandler.route_url + "ping/"

    def get(self):
        return self.jsonify({"status": True, "data": "ping %s success" % self.request.path})

http_handlers.append(PingHandler)
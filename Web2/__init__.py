# encoding: utf-8
# !/usr/bin/python

__author__ = 'zhouheng'
import tornado.web

http_handlers = []

ado_prefix = "/ado"

api_url_prefix = "/dev/api"
status_url_prefix = "/dev/api/status"
test_url_prefix = "/dev/api/test"
bug_url_prefix = "/dev/bug"
right_url_prefix = "/dev/right"
param_url_prefix = "/dev/param"
dev_url_prefix = "/dev"
dms_url_prefix = ""
data_url_prefix = "/data"
log_url_prefix = "/log"
tools_url_prefix = "/tools"
release_url_prefix = "/dev/release"
github_url_prefix = "/github"
chat_url_prefix = "/chat"


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


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.kwargs = {"current_env": "Tornado", "g": GlobalInfo()}

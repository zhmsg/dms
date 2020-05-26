from flask import g, request, current_app
import time
import uuid

from dms.web import FlaskHook
from dms.web.base import REGISTER_DATA

__author__ = 'zhouhenglc'


class TaskHook(FlaskHook):

    priority = 130
    basic_time = 1582268928

    def __init__(self, app):
        FlaskHook.__init__(self, app)
        self.auto_methods = ['POST', 'PUT', 'DELETE']

    @classmethod
    def gen_task_id(cls):
        offset = (time.time() - cls.basic_time) / (3600 * 24)
        prefix = str(int(offset)).zfill(4)
        task_id = prefix + uuid.uuid4().hex
        return task_id

    def required_task_id(self):
        if not request.url_rule:
            return False
        if request.method in self.auto_methods:
            no_task_id = REGISTER_DATA.get('no_task_id', [])
            if request.url_rule.endpoint in no_task_id:
                return False
            return True
        task_id_required = REGISTER_DATA.get('task_id_required', [])
        return request.url_rule.endpoint in task_id_required

    def before_request(self):
        if hasattr(g, 'body'):
            pass

        if self.required_task_id():
            g.task_id = self.gen_task_id()
            self.log.debug('Generate new task_id=%s', g.task_id)
        elif request.view_args and 'task_id' in request.view_args:
            g.task_id = request.view_args['task_id']
            self.log.debug('Get task_id=%s from view args', g.task_id)
        elif 'task_id' in request.args:
            g.task_id = request.args['task_id']
            self.log.debug('Get task_id=%s from request args', g.task_id)
        # TODO verify task_id format

    def after_request(self, response):
        if hasattr(g, 'task_id'):
            response.headers['X-Task-ID'] = g.task_id
        return response

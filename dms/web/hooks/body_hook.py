# encoding: utf-8
# !/usr/bin/python

from flask import g, request


from flask_helper.flask_hook import FlaskHook
from dms.web.base import REGISTER_DATA
from dms.exceptions import InvalidInput


__author__ = 'zhouhenglc'


class BodyHook(FlaskHook):
    priority = 120

    def __init__(self, app):
        FlaskHook.__init__(self, app)
        self.data_key = 'validators'

    def get_validator(self):
        if not request.url_rule:
            return None
        validators = REGISTER_DATA.get(self.data_key, {})
        return validators.get(request.url_rule.endpoint, None)

    def before_request(self):
        if request.method in ['POST', 'PUT', 'DELETE']:
            validator = self.get_validator()
            if request.data:
                g.body = request.json
            else:
                self.log.debug('No data in request body')
            if validator:
                data = g.body if 'body' in g else {}
                vr = validator.validate(data)
                if vr.v_result:
                    self.log.error(vr.v_result)
                    raise InvalidInput(msg=vr.v_result)
                g.body = vr.new_value

    def after_request(self, response):
        return response

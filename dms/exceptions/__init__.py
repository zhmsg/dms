# !/usr/bin/env python
# coding: utf-8


__author__ = 'zhouhenglc'


class DmsException(Exception):
    code = 500
    message = ''

    def __init__(self, detail=None, *args, **kwargs):
        self.msg = self.message % kwargs
        if detail is None:
            self.detail = self.msg
        else:
            self.detail = detail
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        _str = 'msg: %s, detail:%s' % (self.msg, self.detail)
        return _str


class NotFound(DmsException):
    code = 404
    message = 'Not found'


class BadRequest(DmsException):
    code = 400
    message = 'Bad request'


class InvalidInput(BadRequest):
    message = 'Invalid input: %(msg)s'

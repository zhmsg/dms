from flask import make_response, jsonify, g

from dms.exceptions import DmsException

__author__ = 'zhouhenglc'


def handle_500(e):
    code = 500
    error_type = e.__class__.__name__
    data = {'error_type': error_type, 'status': False}
    if isinstance(e, DmsException):
        data['message'] = e.msg
        data['detail'] = e.detail
        code = e.code
    else:
        data['message'] = str(e)
    if hasattr(g, 'task_id'):
        data['task_id'] = g.task_id
    resp = make_response(jsonify(data), code)
    return resp

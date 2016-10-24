#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import pickle
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict


class RedisSession(CallbackDict):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface:
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis_host, prefix, cookie_domain, cookie_name):
        redis = Redis(host=redis_host)
        self.redis = redis
        self.prefix = prefix + ":"
        self.cookie_name = cookie_name
        self.cookie_domain = cookie_domain

    def generate_sid(self):
        return "ado-" + str(uuid4())

    def get_redis_expiration_time(self):
        return timedelta(seconds=300)

    def open_session(self, handler):
        sid = handler.get_cookie(self.cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, handler):
        domain = self.cookie_domain
        if not handler.session:
            self.redis.delete(self.prefix + handler.session.sid)
            if handler.session.modified:
                handler.clear_cookie(self.cookie_name, domain=domain)
            return
        redis_exp = self.get_redis_expiration_time()
        val = self.serializer.dumps(dict(handler.session))
        self.redis.setex(self.prefix + handler.session.sid, val, int(redis_exp.total_seconds()))
        handler.set_cookie(self.cookie_name, handler.session.sid, httponly=True, domain=domain)

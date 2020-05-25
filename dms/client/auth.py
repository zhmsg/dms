# !/usr/bin/env python
# coding: utf-8
import requests

__author__ = 'zhouhenglc'


class _Request(object):

    def __init__(self, session, endpoint):
        self._endpoint = endpoint.rstrip('/')
        self._session = session


    def get(self, url, **kwargs):
        if url.startswith('/'):
            url = '%s%s' % (self._endpoint, url)
        else:
            url = '%s/%s' % (self._endpoint, url)
        response = self._session.get(url, **kwargs)
        try:
            r_data = response.json()
        except Exception as e:
            print(response.text)
            raise e
        return r_data

    def post(self, url, data=None, json=None, **kwargs):
        url = '%s/%s' % (self._endpoint, url)
        response = self._session.post(url, data, json, **kwargs)


class Authorization(object):

    def __init__(self, endpoint_url, user_name, password):
        self.endpoint_url = endpoint_url
        self._user_name = user_name
        self._password = password
        self._req_session = requests.session()
        self.set_default_headers()
        self._login()
        self._request = _Request(self._req_session, self.endpoint_url)

    @property
    def request(self):
        return self._request

    @property
    def session(self):
        return self._req_session

    def set_default_headers(self):
        self._req_session.headers["User-Agent"] = "requests"
        self._req_session.headers['Accept'] = 'application/json'

    def _login(self):
        url = "%s/login/" % self.endpoint_url
        auth_data = {'user_name': self._user_name, 'password': self._password}
        response = self._req_session.post(url, json=auth_data)
        print(response.text)

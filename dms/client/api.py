# !/usr/bin/env python
# coding: utf-8
import queue

__author__ = 'zhouhenglc'


class _DictObject(object):

    def __init__(self, **kwargs):
        self._data = kwargs
        for key, value in kwargs.items():
            if isinstance(value, dict):
                setattr(self, key, _DictObject(**value))
            else:
                setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return self._data.__str__()

    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        return default


class _Object(object):
    URL_PREFIX = '/dev/api'

    def __init__(self, auth):
        self.auth = auth

    def get_url(self, url):
        if url.startswith('/'):
            f_url = '%s%s' % (self.URL_PREFIX, url)
        else:
            f_url = '%s/%s' % (self.URL_PREFIX, url)
        return f_url


class APIPartObject(_Object):

    def __init__(self, auth, part_no):
        _Object.__init__(self, auth)
        self.part_no = part_no

    def load_modules(self):
        response = self.auth.request.get(self.get_url('/module'))


class APIModuleObject(_Object):

    def __init__(self, auth, module_no):
        _Object.__init__(self, auth)
        self.module_no = module_no
        self.api_list = []

    def load_api_list(self):
        params = {'module_no': self.module_no}
        response = self.auth.request.get(self.get_url('/module'),
                                         params=params)
        for item in response['data']['api_list']:
            api_item = APIItemObject(self.auth, item['api_no'])
            api_item.load()
            self.api_list.append(api_item)


class APIItemObject(_Object):

    def __init__(self, auth, api_no):
        _Object.__init__(self, auth)
        self.api_no = api_no
        self._data = {}

    @property
    def basic_info(self):
        return _DictObject(**self._data['basic_info'])

    @property
    def input_examples(self):
        return self._data['input_info']

    @property
    def output_examples(self):
        return self._data['output_info']

    @property
    def body_params(self):
        if 'sub_params' not in self._data['params']['body']:
            return {}
        return self._data['params']['body']['sub_params']

    @property
    def body_params_list(self):
        _p_list = []
        stack = []
        for key, value in self.body_params.items():
            stack.append(value)
        while stack:
            item = stack.pop()
            _p_list.append(item)
            if 'sub_params' in item:
                if isinstance(item['sub_params'], list):
                    for _v in item['sub_params']:
                        stack.append(_v)
                else:
                    for _k, _v in item['sub_params'].items():
                        stack.append(_v)
        return _p_list

    @property
    def path_params(self):
        if 'sub_params' not in self._data['params']['url']:
            return {}
        return self._data['params']['url']['sub_params']

    @property
    def url_params(self):
        if 'sub_params' not in self._data['params']['url_args']:
            return {}
        return self._data['params']['url_args']['sub_params']

    def load(self):
        args = {'api_no': self.api_no, 'rf': 'async'}
        response = self.auth.request.get(self.get_url('/info'),
                                         params=args)
        self._data.update(response['data']['api_info'])
        self.load_params()

    def load_params(self):
        args = {'api_no': self.api_no}
        response = self.auth.request.get(self.get_url('/param'),
                                         params=args)
        self._data.update(params=response['data'])


if __name__ == '__main__':
    from dms.client.auth import Authorization
    auth = Authorization('http://127.0.0.1:2200', 'admin', 'admin')
    # auth = Authorization('http://100.7.50.26:2200', 'admin', 'admin')
    module = APIModuleObject(auth, 32)
    module.load_api_list()

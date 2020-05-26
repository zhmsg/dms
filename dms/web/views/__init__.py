# !/usr/bin/env python
# coding: utf-8
from dms.web.views.develop_api_view import develop_api_bp
from dms.web.views.dms_view import dms_bp

__author__ = 'zhouhenglc'


__all__ = []


for mod_name, mod in dict(locals()).items():
    if mod_name.endswith('_bp'):
        __all__.append(mod)

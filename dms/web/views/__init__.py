# !/usr/bin/env python
# coding: utf-8
from dms.web.views.develop_api_view import develop_api_bp
from dms.web.views.develop_param_view import develop_param_bp
from dms.web.views.develop_test_view import develop_test_bp
from dms.web.views.dms_user_policies_view import user_role_bp
from dms.web.views.dms_view import dms_bp
from dms.web.views.short_link_view import short_link_bp

__author__ = 'zhouhenglc'


__all__ = []


for mod_name, mod in dict(locals()).items():
    if mod_name.endswith('_bp'):
        __all__.append(mod)

# !/usr/bin/env python
# coding: utf-8

import eventlet
import importlib
import os
import sys

script_file_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.join(script_file_path, '..', '..'))

__author__ = 'zhouhenglc'


if __name__ == '__main__':
    sys.path.insert(0, root_dir)
    module_app = importlib.import_module('dms.web.app')
    app = module_app.get_application()
    eventlet.monkey_patch()
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(host='0.0.0.0', port=2200)

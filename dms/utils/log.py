import logging
import logging.config
from logging import Formatter, StreamHandler
from logging.handlers import WatchedFileHandler

import os
import sys


LOG_LEVEL = logging.INFO
LOG_FILE = 'dms.log'
DAEMON = False


__author__ = 'zhouhenglc'


task_fmter = Formatter('%(asctime)s-[%(levelname)s]-'
                       '[%(filename)s::%(funcName)s:line:%(lineno)d]-'
                       '[%(task_id)s]-%(message)s')
long_fmter = Formatter('%(asctime)s-[%(levelname)s]-'
                       '[%(filename)s::%(funcName)s:line:%(lineno)d]-'
                       '%(message)s')
simple_fmter = Formatter('%(asctime)s:%(levelname)s:%(message)s')


task_handler = WatchedFileHandler(LOG_FILE)
task_handler.level = logging.DEBUG
task_handler.setFormatter(task_fmter)

file_handler = WatchedFileHandler(LOG_FILE)
file_handler.level = logging.DEBUG
file_handler.setFormatter(long_fmter)

console_handle = StreamHandler(sys.stdout)
console_handle.level = logging.DEBUG
console_handle.setFormatter(simple_fmter)


def set_logger_as_root(name):
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    if not DAEMON:
        logger.addHandler(console_handle)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    return logger


set_logger_as_root(None)
set_logger_as_root('dms')


def getLogger(name='dms'):
    logger = logging.getLogger(name)
    return logger


def getTaskLogger():
    return getLogger('trident-task')


if __name__ == '__main__':
    getLogger().info('111111')

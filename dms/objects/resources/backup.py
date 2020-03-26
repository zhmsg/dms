# !/usr/bin/env python
# coding: utf-8

import os
import re
from time import time

from smb.SMBConnection import SMBConnection

from dms.objects.resources.base import ResourceManager

__author__ = 'zhouhenglc'


class SMBackup(object):

    def __init__(self, user_name, password, ip, port=139):
        self.user_name = user_name
        self.password = password
        self.ip = ip
        self.port = port
        self.conn = None

    def connect(self):
        conn = SMBConnection(self.user_name, self.password, '', '')
        conn.connect(self.ip, self.port)
        self.conn = conn

    def list_files(self):
        names = self.conn.listPath('openstackXMZ', 'zhouhenglc/dms')
        for sf in names:
            print(sf.filename)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


class BackupManager(ResourceManager):

    NAME = "backup"

    def __init__(self):
        ResourceManager.__init__(self)


if __name__ == '__main__':
    sb = SMBackup('zhouhenglc', '112233a?', '100.7.49.251')
    sb.connect()
    sb.list_files()
    sb.close()

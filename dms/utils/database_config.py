#! /usr/bin/env python
# coding: utf-8

from six.moves import configparser

from dms.utils.config_dir import ConfigDir
from dms.utils.singleton import Singleton


class MysqlConfig(Singleton):
    config_filename = ["mysql.conf", "mysql_app.conf"]

    def __init__(self):
        conf_d = ConfigDir()
        config_path = conf_d.find_config_file(*self.config_filename)
        if config_path is None:
            raise RuntimeError("No profile found in any directory: %s"
                               % " ".join(conf_d.directories))
        self.config_path = config_path
        self.host = ""
        self.port = ""
        self.db_name = ""
        self.charset = ""
        self.user = ""
        self.password = ""
        self.read_user = ""
        self.read_password = ""
        self._read_conf()

    def _read_conf(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        basic_section = "db_basic"
        self.host = config.get(basic_section, "host")
        self.db_name = config.get(basic_section, "name")
        self.port = config.getint(basic_section, "port")

        if config.has_option(basic_section, "charset"):
            self.charset = config.get(basic_section, "charset")
        user_section = "%s_user" % basic_section
        if config.has_section(user_section):
            if config.has_option(user_section, "user"):
                self.user = config.get(user_section, "user")
            if config.has_option(user_section, "password"):
                self.password = config.get(user_section, "password")
        read_user_section = "%s_read_user" % basic_section
        if config.has_section(read_user_section):
            if config.has_option(read_user_section, "user"):
                self.read_user = config.get(read_user_section, "user")
            if config.has_option(user_section, "password"):
                self.read_password = config.get(read_user_section, "password")

    def to_dict(self, read_only=False):
        o = dict(host=self.host)
        if self.port:
            o["port"] = self.port
        if self.charset:
            o["charset"] = self.charset
        if read_only:
            if self.read_user:
                o["user"] = self.read_user
            if self.read_password:
                o["password"] = self.read_password
        else:
            if self.user:
                o["user"] = self.user
            if self.password:
                o["password"] = self.password
        return o


if __name__ == "__main__":
    mysql_config = MysqlConfig()
    print(id(mysql_config))
    mysql_config2 = MysqlConfig()
    print(id(mysql_config2))
    print(mysql_config.to_dict())

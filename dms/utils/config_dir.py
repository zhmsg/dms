#! /usr/bin/env python
# coding: utf-8
import os

from dms.utils.singleton import Singleton


class ConfigDir(Singleton):

    def __init__(self):
        current_dir = os.path.abspath(".")
        script_file = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_file)
        parent_dir = os.path.dirname(script_dir)
        self.directories = [current_dir]
        etc_dir = "/etc/dms"
        if script_dir not in self.directories:
            self.directories.append(script_dir)
        if parent_dir not in self.directories:
            self.directories.append(parent_dir)
        if etc_dir not in self.directories:
            self.directories.append(etc_dir)

    def find_config_file(self, *filename, env_name=None):
        if env_name:
            path = os.environ.get(env_name)
            if os.path.exists(path):
                return path
        for directory in self.directories:
            for name in filename:
                file_path = os.path.join(directory, name)
                if os.path.isfile(file_path):
                    return file_path
        else:
            return None

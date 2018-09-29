#!/usr/bin/env python

# encoding: utf-8

'''
 * Create File Config
 * Created by leixu on 2018/9/28
 * IDE PyCharm
'''
import configparser
import time


class BaseConfig(object):
    pass


class Config(object):
    def __init__(self, static_path=None, url=None):
        self.config = None
        self.p = None
        if static_path:
            self.reload_config_file(static_path)
        elif url:
            self.reload_online(url)

    def reload_online(self, url):
        pass

    def load_dict(self, _dict):
        return

    def reload_config_file(self, path):
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.config.read(path, encoding="utf8")

    def load_str(self, _str):
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.config.read_string(_str)

    def style_json(self):
        pass

    def style_class(self):
        if isinstance(self.config, configparser.ConfigParser):
            _o = BaseConfig()
            for section in self.config.sections():
                setattr(_o, section, BaseConfig())
                for key in self.config.options(section):
                    sub_config = getattr(_o, section)
                    setattr(sub_config, key, self.config.get(section, key))
            return _o
        else:
            pass

    def style_configparser(self):
        return self.config

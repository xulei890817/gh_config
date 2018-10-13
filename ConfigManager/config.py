#!/usr/bin/env python

# encoding: utf-8

'''
 * Create File Config
 * Created by leixu on 2018/9/28
 * IDE PyCharm
'''
import configparser
import time
from threading import Thread


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

    def watch_config_on_redis(self, redis_client, service_name, update_config_func):
        config_init_flag = False

        p = redis_client.pubsub(ignore_subscribe_messages=True)

        def sub():
            nonlocal config_init_flag
            p.subscribe("config_change_service-" + service_name)
            p.subscribe("config_error_service-" + service_name)
            while True:
                message = p.get_message()
                if message:
                    print(message)
                    channel = message["channel"].decode()
                    if channel.startswith("config_change_service"):
                        c = Config()
                        c.load_str(message["data"].decode())
                        config = getattr(c.style_class(), service_name)
                        update_config_func(config)
                        config_init_flag = True
                time.sleep(0.5)

        Thread(target=sub).start()
        redis_client.publish("config_get_service-" + service_name, None)

        warn_line = 10
        counter = 0
        while not config_init_flag:
            time.sleep(0.5)
            counter = counter + 1
            if counter >= warn_line:
                raise Exception("Please start  ConfigServer first!")
        print("config get successfully")

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

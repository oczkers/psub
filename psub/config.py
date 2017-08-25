# -*- coding: utf-8 -*-

"""
psub.config
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub config methods.

"""

import yaml
from os.path import expanduser

from .exceptions import PsubError


class Config(object):
    def __init__(self, filename='psub.yml', path=None):  # default filename
        # TODO: config in home
        if not path:
            path = expanduser('~/.config/')
        self.config_file = path + filename
        self._load()

    def _load(self):
        try:
            config = yaml.safe_load(open(self.config_file, 'r'))
        except IOError as e:  # FileNotFoundError doesn't exists in python2 AND pypy3
            print(e)  # config does not exists, load default
            config = {}
        except yaml.YAMLError as e:
            print(e)  # config cannot be loaded
            raise PsubError('Config cannot be loaded, probably broken.')

        self.destination = config.get('destination', '.')
        # TODO?: score
        # TODO: language
        # TODO: encoding
        # TODO: format
        self.provider = config.get('provider', 'napisy24')
        self.napisy24 = config.get('napisy24', {'cookies': None,
                                                'username': None,
                                                'passwd': None})
        self.napiprojekt = config.get('napiprojekt', {'username': None,
                                                      'passwd': None})
        # self.save()  # save to add new values, correct structure etc.

    def save(self):
        # TODO: autosave on change any param
        config = {'destination': self.destination,
                  'provider': self.provider,
                  'napisy24': self.napisy24,
                  'napiprojekt': self.napiprojekt}
        yaml.safe_dump(config, open(self.config_file, 'w'), default_flow_style=False)

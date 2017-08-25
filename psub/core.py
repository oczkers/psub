# -*- coding: utf-8 -*-

"""
psub.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub basic methods.

"""


import re

from .config import Config
from .logger import logger
from .providers import napisy24, napiprojekt


class Core(object):
    def __init__(self, debug=False):
        logger(save=debug)  # init root logger
        self.logger = logger(__name__)
        self.config = Config()  # TODO: config_file
        # self.provider = napisy24.Provider()

    def _parseFilename(self, filename):
        """Parse filename. Returns {title, year, group}."""
        # TODO: path
        print('Filename: ' + filename)  # DEBUG
        filename = filename.lower().replace(' ', '.')
        data = {}
        rc = re.match('(.+?)\.+s([0-9]{2})e([0-9]{2})\..+\-(.+?)\..{2,4}', filename)
        if rc:  # tvshow
            data['category'] = 'tvshow'
            data['season'] = rc.group(2)
            data['episode'] = rc.group(3)
            data['group'] = rc.group(4)
        else:  # movie
            rc = re.match('(.+?)\.([0-9]{4})\..+\-(.+?)\..{2,4}', filename)
            data['category'] = 'movie'
            data['year'] = rc.group(2)
            data['group'] = rc.group(3)
        data['title'] = rc.group(1)
        print('Parsed: ')  # DEBUG
        print(data)  # DEBUG
        return data

    def download(self, filename, provider=None):
        """Downloads subtitles."""
        # TODO: destination
        # TODO: language
        # TODO: format + conversion
        # TODO: encoding + conversion
        # TODO: imdb_id
        if not provider:
            provider = self.config.provider
        if provider == 'napisy24':  # TODO: getattr
            self.provider = napisy24.Provider(username=self.config.napisy24['username'], passwd=self.config.napisy24['passwd'])
        elif provider == 'napiprojekt':
            self.provider = napiprojekt.Provider(username=self.config.napiprojekt['username'], passwd=self.config.napiprojekt['passwd'])
        else:
            print('Unknown provider.')

        data = self._parseFilename(filename)
        fc = self.provider.download(filename=filename, category=data['category'], title=data['title'], year=data.get('year'), season=data.get('season'), episode=data.get('episode'), group=data['group'])
        open(filename.replace('.mkv', f'.pl.{fc["ext"]}'), 'wb').write(fc['data'])  # TODO: not allways mkv

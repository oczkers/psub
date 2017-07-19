# -*- coding: utf-8 -*-

"""
psub.provider
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub provider base methods.

"""

import requests

from ..logger import logger


# chrome 58 @ win10
headers = {  # TODO?: move to config
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch, br',
    'Accept-Language': 'en-US,en;q=0.8',
    # 'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.1',
    'Connection': 'keep-alive',
    # 'Keep-Alive': '300',
    'DNT': '1',
}


class BaseProvider(object):
    def __init__(self, username=None, passwd=None, logger_name=__name__):  # remove username, passwd?
        # self.logger = logger(child=True)
        self.logger = logger(logger_name)
        self.r = requests.Session()
        self.r.headers = headers

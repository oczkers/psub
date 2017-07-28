# -*- coding: utf-8 -*-

"""
psub.providers.napiprojekt
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub napiprojekt.pl provider methods.

"""

# import re
# import lzma  # python 3.3+
# import requests
from hashlib import md5
from lxml import etree
from base64 import b64decode
# from bs4 import BeautifulSoup
# from random import random
# from io import BytesIO
# from zipfile import ZipFile

from . import BaseProvider
from ..exceptions import PsubError


def fhash(z):  # raise 'Not a MD5 sum' unless md5sum =~ /^[0-9a-f]{32}$/
    idx = [0xe, 0x3, 0x6, 0x8, 0x2]
    mul = [2, 2, 5, 4, 3]
    add = [0, 0xd, 0x10, 0xb, 0x5]

    b = []
    for i in range(len(idx)):
        a = add[i]
        m = mul[i]
        i = idx[i]

        t = a + int(z[i], 16)
        v = int(z[t:t + 2], 16)
        b.append(("%x" % (v * m))[-1])

    return ''.join(b)


class Provider(BaseProvider):
    def __init__(self, username, passwd):  # TODO: username & password is not needed when cookies are available
        super().__init__(logger_name=__name__)

    def download(self, filename, category, title, year=None, season=None, episode=None, group=None):  # TODO: params
        """Download subtitle."""
        # MicroDVD (txt/sub)
        # inspired by https://github.com/CaTzil/service.subtitles.napiprojekt/blob/master/resources/lib/NapiProjekt.py
        with open(filename, 'rb') as f:
            md5hash = md5(f.read(10485760)).hexdigest()
        params = {'mode': '1',
                  'client': 'NapiProjektPython',
                  'client_ver': '0.1',
                  'downloaded_subtitles_id': md5hash,
                  'downloaded_subtitles_txt': '1',
                  'downloaded_subtitles_lang': 'PL'}  # ENG
        rc = self.r.post('http://napiprojekt.pl/api/api-napiprojekt3.php', data=params).text
        # open('psub.log', 'wb').write(rc)  # DEBUG
        if 'content' not in rc:
            raise PsubError('Not found.')
            return False
        rc = etree.fromstring(rc)
        rc = b64decode(rc[1][6].text)
        # TODO: txt/sub->srt
        return {'data': rc,
                'ext': 'sub'}

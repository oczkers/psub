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
        # self.login(username, passwd)

    # def login(self, username, passwd):
    #     # TODO: save cookies
    #     pass

    # def download(self, category, title, year=None, season=None, episode=None, group=None):  # TODO: params
    #     """Search subtitles. Returns all results."""
    #     with open('/mnt/gdrive/movies/sleep.tight.2011.1080p.bluray.x264-geckos.mkv', 'rb') as f:
    #         md5hash = md5(f.read(10485760)).hexdigest()
    #     params = {'l': 'PL',  # ENG
    #               'f': md5hash,
    #               't': fhash(md5hash),
    #               'v': 'other',
    #               'kolejka': 'false',
    #               'nick': '',
    #               'pass': '',
    #               'napios': 'Linux'}
    #     rc = self.r.get('http://napiprojekt.pl/unit_napisy/dl.php', params=params).content  # 7z with password iBlm8NTigvru0Jr0  OR  NPc/NPc0 if not found/wrong request
    #     # bzip2 7zaes
    #     open('data.7z', 'wb').write(rc)
    #     lz = lzma.LZMADecompressor()
    #     rc = lz.decompress(rc)
    #     open('sub.txt', 'wb').write(rc)
    #     # BytesIO(rc)
    #     asdsads

    def download(self, filename, category, title, year=None, season=None, episode=None, group=None):  # TODO: params
        """Download subtitle."""
        # MicroDVD (txt)
        # with open('/mnt/gdrive/movies/sleep.tight.2011.1080p.bluray.x264-geckos.mkv', 'rb') as f:
        with open(filename, 'rb') as f:
            md5hash = md5(f.read(10485760)).hexdigest()
        params = {'mode': '1',
                  'client': 'NapiProjektPython',
                  'client_ver': '0.1',
                  'downloaded_subtitles_id': md5hash,
                  'downloaded_subtitles_txt': '1',
                  'downloaded_subtitles_lang': 'PL'}  # ENG
        rc = self.r.post('http://napiprojekt.pl/api/api-napiprojekt3.php', data=params).content  # 7z with password iBlm8NTigvru0Jr0  OR  NPc/NPc0 if not found/wrong request
        # open('psub.log', 'wb').write(rc)  # DEBUG
        if 'content' not in rc:
            raise PsubError('Not found.')
            return False
        rc = etree.fromstring(rc)
        rc = b64decode(rc[1][6].text)
        # TODO: txt->srt
        return {'data': rc,
                'ext': 'txt'}

# -*- coding: utf-8 -*-

"""
psub.providers.napisy24
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub napisy24.pl provider methods.

"""

import re
from bs4 import BeautifulSoup
# from random import random

from . import BaseProvider
from ..exceptions import PsubError


class Provider(BaseProvider):
    def __init__(self, username=None, passwd=None):  # TODO: username & password is not needed when cookies are available
        super().__init__(logger_name=__name__)
        if username and passwd:
            self.login(username, passwd)

    def login(self, username, passwd):
        # TODO: save cookies
        rc = self.r.get('http://napisy24.pl').text
        cbsecuritym3 = re.search('name="cbsecuritym3" value="(.+?)"', rc).group(1)
        data = {'option': 'com_comprofiler',
                'view': 'login',
                'op2': 'login',
                'return': 'B:aHR0cDovL25hcGlzeTI0LnBsLw==',  # somekind of url hash?
                'message': 0,
                'loginfrom': 'loginmodule',
                'cbsecuritym3': cbsecuritym3,
                'username': username,
                'passwd': passwd,
                'remember': 'yes',
                'Submit': ''}
        rc = self.r.post('http://napisy24.pl/cb-login', data=data).text
        if 'logout' not in rc:
            open('psub.log', 'w').write(rc)
            raise PsubError('Unknown error during login.')

    def search(self, category, title, year=None, season=None, episode=None, group=None):
        """Search subtitle."""
        # TODO: tvshow
        # TODO: language
        # TODO: score
        # TODO: refactorization
        # TODO?: score boost for well know author
        subs = []
        if category == 'movie':
            search = title
            typ = 1
        elif category == 'tvshow':
            search = '%s %sx%s' % (title, season, episode)
            typ = 2
        else:
            raise PsubError('Unknown category.')
        # srand = str(random() * 83649864)  # don't ask me...
        # files = {'send': 'Szukaj',
        #          'search': title,
        #          'srand': srand}
        # rc = self.r.post('http://napisy24.pl/szukaj', files=files).text
        data = {'page': 1,
                'lang': 0,  # polish
                'search': search,
                'typ': typ}
        rc = self.r.post('http://napisy24.pl/szukaj', data=data).text
        open('psub.log', 'w').write(rc)
        bs = BeautifulSoup(rc, 'lxml')  # TODO?: ability to change engine
        results = bs.select('[data-napis-id]')
        for rc in results:  # based on CaTzil's kodi plugin
            rc_id = rc['data-napis-id']
            rc_title = rc.find('div', {'class': 'uu_oo_uu'}).get_text().title()  # TODO?: parse for tvshow ('Bloodline' Episode #2.4)
            releases = rc.find('div', attrs={'data-releases': True})['data-releases'].split('<br> ')
            groups = []
            for i in releases:
                rc2 = re.match('(.+?)\.(.+?)\-(.+?)', i)  # source (webrip)  |  codecs (x264.mp3)  |  group (fleet)
                groups.append(rc2.group(3))
            rc2 = rc.find('div', {'class': 'infoColumn2'}).contents
            # rc_year = rc2[0].replace('\t', '').replace('\n', '')
            rc_time = rc2[2].replace('\t', '').replace('\n', '')  # TODO: parse
            rc_resolution = rc2[4].replace('\t', '').replace('\n', '')  # this is probably useless
            rc_fps = rc2[6].replace('\t', '').replace('\n', '')
            rc_size = rc2[8].replace('\t', '').replace('\n', '')  # TODO: parse

            for rc3 in [releases]:  # TODO: refactorization - [sub for sub in releases if rc_year == year]?
                # TODO?: check year     if rc_year == year:
                subs.append({'id': rc_id,
                             'title': rc_title,
                             # 'release': rc3,  # use group/source/codec instead
                             'groups': groups,
                             'time': rc_time,
                             'resolution': rc_resolution,
                             'fps': rc_fps,
                             'size': rc_size})
        print('RESULTS: ')
        print(subs)
        return subs

    def download(self, category, title, year=None, season=None, episode=None, group=None):
        """Download subtitle."""
        # TODO: sort based on group, size/time, fps, codecs
        # mdvd | MicroDVD
        # mpl2 | MPL2
        # sr | SubRip
        # sru | SubRip (UTF-8)  <-- best, should be default
        # /download?napisId=64124&typ=sru
        return self.search(category=category, title=title, year=year, season=season, episode=episode, group=group)

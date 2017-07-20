# -*- coding: utf-8 -*-

"""
psub.providers.napisy24
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub napisy24.pl provider methods.

"""

import re
import requests
from bs4 import BeautifulSoup
# from random import random
from io import BytesIO
from zipfile import ZipFile

from . import BaseProvider
from ..exceptions import PsubError


class Provider(BaseProvider):
    def __init__(self, username, passwd):  # TODO: username & password is not needed when cookies are available
        super().__init__(logger_name=__name__)
        self.login(username, passwd)

    def login(self, username, passwd):
        # TODO: save cookies
        if self.config.napisy24['cookies']:
            self.r.cookies = requests.cookies.cookiejar_from_dict(self.config.napisy24['cookies'])
        elif not (username or passwd):
            raise PsubError('Username & password or cookies is required for this provider.')  # TODO: PsubError -> PsubProviderError
        else:  # TODO: _login
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
            if 'logout' in rc:
                self.config.napisy24['cookies'] = self.r.cookies.get_dict()  # this is very simple method, no domain, expire date is saved
                self.config.save()
                return True
            else:
                open('psub.log', 'w').write(rc)
                raise PsubError('Unknown error during login.')

    def searchAll(self, category, title, year=None, season=None, episode=None):
        """Search subtitles. Returns all results."""
        # TODO: language
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
        # open('psub.log', 'w').write(rc)  # DEBUG
        bs = BeautifulSoup(rc, 'lxml')  # TODO?: ability to change engine
        results = bs.select('[data-napis-id]')
        if len(results) == 0:  # TODO: dont raise, just return false/none
            raise PsubError('No subtitles found.')
        for rc in results:  # based on CaTzil's kodi plugin
            rc_id = rc['data-napis-id']
            rc_title = rc.find('div', {'class': 'uu_oo_uu'}).get_text().title()  # TODO?: parse for tvshow ('Bloodline' Episode #2.4)
            releases = rc.find('div', attrs={'data-releases': True})['data-releases'].split('<br> ')
            groups = []
            for i in releases:  # TODO: refactorization - oneliner
                if i != 'niescenowy':
                    print(i)
                    # rc2 = re.match('^([0-9]{3,4}p)?\.?(.*?)\.?(.+)[\-\.]{1}(.+?)$', i.lower())  # quality (1080p)  |  source (webrip)  |  codecs (x264.mp3)  |  group (fleet)
                    # groups.append(rc2.group(4))
                    groups.append(re.match('^.+[\-\.]{1}(.+?)$', i.lower()).group(1))
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
        # print('RESULTS: ')  # DEBUG
        # print(subs)  # DEBUG
        return subs

    def download(self, category, title, year=None, season=None, episode=None, group=None):
        """Download subtitle."""
        # TODO: sort based on group, size/time, fps, codecs
        # mdvd | MicroDVD
        # mpl2 | MPL2
        # sr | SubRip
        # sru | SubRip (UTF-8)  <-- best, should be default
        # /download?napisId=64124&typ=sru
        sub = self.search(category=category, title=title, year=year, season=season, episode=episode, group=group)
        params = {'napisId': sub['id'],
                  'typ': 'sru'}
        print(params)  # DEBUG
        self.r.headers['Referer'] = 'http://napisy24.pl'
        rc = self.r.get('http://napisy24.pl/download', params=params).content  # TODO: stream
        # open('sub.zip', 'wb').write(rc)
        fc = ZipFile(BytesIO(rc))
        for i in fc.namelist():  # search for subtitle (there are might be url, nfo etc.)
            if i[-3:] == 'srt':
                return fc.open(i).read()

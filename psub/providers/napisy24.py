# -*- coding: utf-8 -*-

"""
psub.providers.napisy24
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub napisy24.pl provider methods.

"""

import re

from . import BaseProvider
from ..exceptions import PsubError


class Provider(BaseProvider):
    def __init__(self, username, passwd):  # TODO: username & password is not needed when cookies are available
        super().__init__(logger_name=__name__)
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

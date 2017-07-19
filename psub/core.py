# -*- coding: utf-8 -*-

"""
psub.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the psub basic methods.

"""


from .logger import logger


class Core(object):
    def __init__(self, debug=False):
        logger(save=debug)  # init root logger
        self.logger = logger(__name__)
        pass

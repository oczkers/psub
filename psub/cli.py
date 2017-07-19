# -*- coding: utf-8 -*-

"""
psub
====

Usage:
    psub [options]

Options:
    -h, --help                          Show this screen.
    --version                           Show version.
    --debug                             Enable debug.  # TODO: enable debug automatically if not daemon
    -c FILE, --config FILE              Config file. [default: ~/.config/psub.yml]  # TODO: implement
    -d DIR, --destination DIR           Destination dir for torrent files. [default: .]
    -p PROVIDER, --provider PROVIDER    Choose provider.
"""

# import sys
from docopt import docopt

from . import __title__, __version__
# from .core import Core


version_text = '%s v%s' % (__title__, __version__)


def __main__():
    args = docopt(__doc__, version=version_text)
    print(args)


if __name__ == '__main__':
    __main__()

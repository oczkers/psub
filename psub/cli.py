# -*- coding: utf-8 -*-

"""
psub
====

Usage:
    psub [options] FILE...

Options:
    -h, --help                          Show this screen.
    --version                           Show version.
    --debug                             Enable debug.  # TODO: enable debug automatically if not daemon
    -c FILE, --config FILE              Config file. [default: ~/.config/psub.yml]  # TODO: implement
    -d DIR, --destination DIR           Destination dir for torrent files. [default: .]
    -p PROVIDER, --provider PROVIDER    Choose provider [default: napisy24].  # TODO: default provider should not require account
"""

# import sys
from docopt import docopt

from . import __title__, __version__
from .core import Core


version_text = '%s v%s' % (__title__, __version__)


def __main__():
    # TODO: destination
    args = docopt(__doc__, version=version_text)
    print(args)
    psub = Core(debug=args['--debug'])
    for f in args['FILE']:
        psub.download(f, provider=args['--provider'])


if __name__ == '__main__':
    __main__()

# TODO: drop docopt, use click
# https://github.com/pallets/click

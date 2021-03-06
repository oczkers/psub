====
psub
====

.. image:: https://img.shields.io/pypi/v/psub.svg
    :target: https://pypi.python.org/pypi/psub

.. image:: https://img.shields.io/pypi/l/psub.svg
    :target: https://pypi.python.org/pypi/psub

.. image:: https://img.shields.io/pypi/pyversions/psub.svg
    :target: https://pypi.python.org/pypi/psub

.. image:: https://travis-ci.org/oczkers/psub.png?branch=master
    :target: https://travis-ci.org/oczkers/psub

.. image:: https://codecov.io/github/oczkers/psub/coverage.svg?branch=master
    :target: https://codecov.io/github/oczkers/psub
    :alt: codecov.io

.. image:: https://api.codacy.com/project/badge/Grade/0c42351a19b44bb092932aba796a9c2f
    :target: https://www.codacy.com/app/oczkers/psub?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=oczkers/psub&amp;utm_campaign=Badge_Grade

psub is a very simple subtitle downloader for movies and tv shows. Some day it is going to be merged into pdeo.
It is written entirely in Python.



Documentation
=============

Documentation might be available someday at http://psub.readthedocs.org/.


Installation
============

(not working yet)

.. code-block:: bash

    computer ~ # pip install psub

OR download and invoke installation manually

.. code-block:: bash

    computer ~ # python setup.py install


Usage
=====

Look at psub/cli.py for more info.

.. code-block:: bash

  computer ~ # ls
    True.Detective.S02E01.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E04.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E07.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv
    True.Detective.S02E02.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E05.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E08.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv
    True.Detective.S02E03.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E06.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv
  computer ~ # psub *
    ...
  computer ~ # ls
    True.Detective.S02E01.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E04.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E07.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv
    True.Detective.S02E01.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt  True.Detective.S02E04.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt  True.Detective.S02E07.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt
    True.Detective.S02E02.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E05.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E08.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv
    True.Detective.S02E02.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt  True.Detective.S02E05.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt  True.Detective.S02E08.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt
    True.Detective.S02E03.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv  True.Detective.S02E06.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.mkv
    True.Detective.S02E03.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt  True.Detective.S02E06.1080p.WEB-DL.DD5.1.H.264-WAREZNiK.srt


List of providers
-----------------

- napisy24
- napiprojekt
- opensubtitles


Development
===========


License
-------

GNU GPLv3

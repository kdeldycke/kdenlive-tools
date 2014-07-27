===============================
Kdenlive tools
===============================

.. image:: http://img.shields.io/travis/kdeldycke/kdenlive-tools/master.png
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/kdeldycke/kdenlive-tools

.. See: http://www.appveyor.com/docs/status-badges

.. image:: https://ci.appveyor.com/api/projects/status/<security-token>/branch/master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/kdeldycke/kdenlive-tools

.. image:: http://img.shields.io/coveralls/kdeldycke/kdenlive-tools/master.png
    :alt: Coverage Status
    :target: https://coveralls.io/r/kdeldycke/kdenlive-tools

.. image:: http://img.shields.io/pypi/v/kdenlive-tools.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/kdenlive-tools

.. image:: http://img.shields.io/pypi/dm/kdenlive-tools.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/kdenlive-tools

Command line tool to fiddle with kdenlive projects.

* List producers.
* Replace producer's clips.
* Free software: BSD license.


Installation
============

First, if the ``python-lxml`` package is not installed on your system, you will
need XML libraries::

    $ sudo aptitude install libxml2-dev libxslt-dev zlib1g-dev

Only then you'll be able to install the package and its python dependencies::

    $ pip install kdenlive-tools


Documentation
=============

https://kdenlive-tools.readthedocs.org/


Development
===========

To run the all tests run::

    tox

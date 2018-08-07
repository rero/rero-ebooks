# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Ebooks repository for RERO."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

DATABASE = "postgresql"
ELASTICSEARCH = "elasticsearch6"
INVENIO_VERSION = "3.0.0"

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.4.1',
    'isort>=4.3',
    'mock>=2.0.0',
    'pydocstyle>=2.0.0',
    'pytest-cov>=2.5.1',
    'pytest-invenio>=1.0.2,<1.1.0',
    'pytest-mock>=1.6.0',
    'pytest-pep8>=1.0.6',
    'pytest-random-order>=0.5.4',
    'pytest>=3.3.1',
    'selenium>=3.4.3',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.4.0',
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'Flask-Debugtoolbar>=0.10.1',
    'invenio[{db},{es},base,auth,metadata]~={version}'.format(
        db=DATABASE, es=ELASTICSEARCH, version=INVENIO_VERSION),
    'invenio-oaiharvester>=1.0.0a4'
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('rero_ebooks', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='rero-ebooks',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='rero-ebooks Invenio',
    license='MIT',
    author='RERO',
    author_email='software@rero.ch',
    url='https://github.com/rero/rero-ebooks',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'rero-ebooks = invenio_app.cli:cli',
        ],
        'invenio_base.blueprints': [
            'rero_ebooks = rero_ebooks.views:blueprint',
        ],
        'invenio_config.module': [
            'rero_ebooks = rero_ebooks.config',
        ],
        'invenio_i18n.translations': [
            'messages = rero_ebooks',
        ],
        'invenio_pidstore.minters': [
            'ebook = rero_ebooks.minters:ebook_pid_minter',
        ],
        'invenio_pidstore.fetchers': [
            'ebook = rero_ebooks.fetchers:ebook_pid_fetcher',
        ],
        'invenio_search.mappings': [
            'ebooks = rero_ebooks.mappings',
        ],
        'dojson.cli.rule': [
            'cantookmarc21 = rero_ebooks.dojson.marc21:marc21',
        ],
        'rero_ebooks.marc21': [
            'bdleader = rero_ebooks.dojson.marc21.fields.bdleader',
            'bd00x = rero_ebooks.dojson.marc21.fields.bd00x',
            'bd01x09x = rero_ebooks.dojson.marc21.fields.bd01x09x',
            'bd1xx = rero_ebooks.dojson.marc21.fields.bd1xx',
            'bd20x24x = rero_ebooks.dojson.marc21.fields.bd20x24x',
            'bd25x28x = rero_ebooks.dojson.marc21.fields.bd25x28x',
            'bd3xx = rero_ebooks.dojson.marc21.fields.bd3xx',
            'bd4xx = rero_ebooks.dojson.marc21.fields.bd4xx',
            'bd5xx = rero_ebooks.dojson.marc21.fields.bd5xx',
            'bd6xx = rero_ebooks.dojson.marc21.fields.bd6xx',
            'bd70x75x = rero_ebooks.dojson.marc21.fields.bd70x75x',
            'bd76x78x = rero_ebooks.dojson.marc21.fields.bd76x78x',
            'bd80x83x = rero_ebooks.dojson.marc21.fields.bd80x83x',
            'bd84188x = rero_ebooks.dojson.marc21.fields.bd84188x'
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
    ],
)

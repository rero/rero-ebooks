# -*- coding: utf-8 -*-
#
# This file is part of RERO Ebooks.
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# RERO Ebooks is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RERO Ebooks; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Ebooks repository for RERO."""

import os

from setuptools import find_packages, setup
from setuptools.command.egg_info import egg_info


class EggInfoWithCompile(egg_info):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog()
        option_dict = self.distribution.get_option_dict('compile_catalog')
        if option_dict.get('domain'):
            compiler.domain = [option_dict['domain'][1]]
        else:
            compiler.domain = ['messages']
        compiler.use_fuzzy = True
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()


readme = open('README.rst').read()

INVENIO_VERSION = "3.0.0"

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
        'invenio_assets.bundles': [
            'rero_ebooks_css = rero_ebooks.bundles:ebooks_css',
        ],
        'invenio_base.apps': [
            'rero_ebooks = rero_ebooks:ReroEBooks',
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
        'flask.commands': [
            'oaiharvester = rero_ebooks.cli:oaiharvester'
            'records = rero_ebooks.cli:records',
            'oaiharvester = rero_ebooks.cli:oaiharvester'
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
        'invenio_celery.tasks': [
                'rero_ebooks = rero_ebooks.tasks'
        ]

    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)

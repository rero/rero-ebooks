# -*- coding: utf-8 -*-
#
# RERO EBOOKS
# Copyright (C) 2020 RERO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

INVENIO_VERSION = "3.4.1"

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
        'invenio_assets.webpack': [
            'rero_ebooks_theme = rero_ebooks.theme.webpack:theme',
        ],
        'invenio_base.apps': [
            'rero_ebooks = rero_ebooks:ReroEBooks',
        ],
        'invenio_base.blueprints': [
            'rero_ebooks = rero_ebooks.theme.views:blueprint',
        ],
        'invenio_base.api_blueprints': [
            'api_rero_ebooks = rero_ebooks.theme.views:api_blueprint',
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
            'tomarc21 = dojson.contrib.to_marc21:to_marc21',
            'cantookmarc21 = rero_ebooks.dojson.marc21:marc21',
            'cantookjson = rero_ebooks.dojson.json.model:cantook_json'
        ],
        'dojson.cli.dump': [
            'pjson = rero_ebooks.dojson.utils:dump'
        ],

        'flask.commands': [
            'oaiharvester = rero_ebooks.cli:oaiharvester',
            'apiharvester = rero_ebooks.apiharvester.cli:apiharvester'
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
        'invenio_db.models': [
            'apiharvester = rero_ebooks.apiharvester.models'
        ],
        'invenio_celery.tasks': [
            'rero_ebooks = rero_ebooks.tasks',
            'apiharvester = rero_ebooks.apiharvester.tasks'
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
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
    ],
)

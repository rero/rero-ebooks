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

"""Common pytest fixtures and plugins."""

import json
from os.path import dirname, join

import pytest

from rero_ebooks.apiharvester.models import ApiHarvestConfig
from rero_ebooks.apiharvester.utils import api_source

pytest_plugins = ("celery.contrib.pytest", )


@pytest.fixture(scope='module')
def es(appctx):
    """Setup and teardown all registered Elasticsearch indices.

    Scope: module
    This fixture will create all registered indexes in Elasticsearch and remove
    once done. Fixtures that perform changes (e.g. index or remove documents),
    should used the function-scoped :py:data:`es_clear` fixture to leave the
    indexes clean for the following tests.
    """
    from invenio_search import current_search, current_search_client
    from invenio_search.errors import IndexAlreadyExistsError

    try:
        list(current_search.put_templates())
    except IndexAlreadyExistsError:
        current_search_client.indices.delete_template('*')
        list(current_search.put_templates())

    try:
        list(current_search.create())
    except IndexAlreadyExistsError:
        list(current_search.delete(ignore=[404]))
        list(current_search.create())
    current_search_client.indices.refresh()

    try:
        yield current_search_client
    finally:
        current_search_client.indices.delete(index='*')
        current_search_client.indices.delete_template('*')


@pytest.fixture(scope="module")
def data():
    """Init data."""
    with open(join(dirname(__file__), 'data/data.json')) as f:
        data = json.load(f)
        return data


@pytest.fixture(scope="module")
def apiharvester_config_vs(data):
    """Config for VS."""
    return data.get('apiharvester_config_vs')


@pytest.fixture(scope="module")
def apiharvester_config_nj(data):
    """Json response NJ."""
    return data.get('apiharvester_config_nj')


@pytest.fixture(scope="module")
def apiharvester_apiresponse_vs(data):
    """Json response VS."""
    return data.get('apiresponse_vs')


@pytest.fixture(scope='module')
def config_vs(apiharvester_config_vs):
    """Create api config VS."""
    api_source(
        name='VS',
        url=apiharvester_config_vs['url'],
        classname=apiharvester_config_vs['classname'],
        code=apiharvester_config_vs['code'],
        update=True)
    config = ApiHarvestConfig.query.filter_by(name='VS').first()
    return config


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    from invenio_app.factory import create_api

    return create_api


@pytest.fixture(scope='module')
def app_config(app_config):
    """Create temporary instance dir for each test."""
    app_config['RATELIMIT_STORAGE_URL'] = 'memory://'
    app_config['ACCOUNTS_USE_CELERY'] = False,
    app_config['CACHE_TYPE'] = 'simple'
    app_config['SEARCH_ELASTIC_HOSTS'] = None
    return app_config

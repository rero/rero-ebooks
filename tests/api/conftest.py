# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest fixtures and plugins for the API application."""

from __future__ import absolute_import, print_function

import pytest
from invenio_app.factory import create_api


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_api


@pytest.fixture(scope='module')
def app_config(app_config):
    """Overwrite default configuration."""
    app_config['PIDSTORE_RECID_FIELD'] = 'pid'
    return app_config


@pytest.yield_fixture()
def cdf_record():
    """La-chaux-de-fonds record."""
    yield {
        '__order__': [
            'other_standard_identifier',
            'electronic_location_and_access'
        ],
        'other_standard_identifier': [
            {
                '__order__': [
                    'standard_number_or_code'
                ],
                'standard_number_or_code':
                    'http://cantookstation.com/resources/'
                    '5788be89dde6b2d458f42b35'
            }
        ],
        'electronic_location_and_access': [
            {
                '__order__': [
                    'uniform_resource_identifier',
                    'access_method',
                    'relationship',
                ],
                'relationship': 'Resource',
                'access_method': 'HTTP',
                'uniform_resource_identifier': [
                    'http://la-chaux-de-fonds.ebibliomedia.ch/resources/'
                    '5788be89dde6b2d458f42b35'
                ],
            }
        ],
    }


@pytest.yield_fixture()
def dojson_like_cdf_record():
    """La-chaux-de-fonds record."""
    yield {
        '__order__': (
            'other_standard_identifier',
            'electronic_location_and_access',
        ),
        'other_standard_identifier': [
            {
                '__order__': (
                    'standard_number_or_code',
                ),
                'standard_number_or_code':
                    'http://cantookstation.com/resources/'
                    '5788be89dde6b2d458f42b35'
            }
        ],
        'electronic_location_and_access': [
            {
                '__order__': (
                    'uniform_resource_identifier',
                    'access_method',
                    'relationship',
                ),
                'relationship': 'Resource',
                'access_method': 'HTTP',
                'uniform_resource_identifier': (
                    'http://la-chaux-de-fonds.ebibliomedia.ch/resources/'
                    '5788be89dde6b2d458f42b35',
                ),
            }
        ],
    }


@pytest.yield_fixture()
def mv_record():
    """Mediatheque-valais record."""
    yield {
        '__order__': [
            'other_standard_identifier',
            'electronic_location_and_access'
        ],
        'other_standard_identifier': [
            {
                '__order__': [
                    'standard_number_or_code'
                ],
                'standard_number_or_code':
                    'http://cantookstation.com/resources/'
                    '5788be89dde6b2d458f42b35'
            }
        ],
        'electronic_location_and_access': [
            {
                '__order__': [
                    'uniform_resource_identifier',
                    'access_method',
                    'relationship',
                ],
                'relationship': 'Resource',
                'access_method': 'HTTP',
                'uniform_resource_identifier': [
                    'http://mediatheque-valais.ebibliomedia.ch/resources/'
                    '5788be89dde6b2d458f42b35'
                ],
            }
        ],
    }

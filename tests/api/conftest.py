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

"""Pytest fixtures and plugins for the API application."""

from __future__ import absolute_import, print_function

import pytest


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


@pytest.yield_fixture()
def cantook_mv_record():
    """Mediatheque-valais Cantook record."""
    yield {
        "title": "Sylvothérapie : le pouvoir bienfaisant des arbres",
        "title_prefix": None,
        "title_sort": "sylvotherapie : le pouvoir bienfaisant des arbres",
        "subtitle": None,
        "description": None,
        "summary": "Le besoin actuel de reconnexion avec la nature ...",
        "comments": None,
        "tags": [],
        "back_cover": "",
        "back_cover_large": None,
        "cover": "http://images.immateriel.fr/covers/BH9WPJ8.png",
        "cover_large": None,
        "flipbook":
        "http://livre.immateriel.fr/BH9WPJ8?no_sign_in=true&no_buy_link=true",
        "languages": [
            "fre"
        ],
        "page_count": 160,
        "translated_from": "",
        "contributors": [
            {
                "first_name": "Jean-Marie",
                "last_name": "Defossez",
                "nature": "author",
                "country": "",
                "biography": "<p>Jean-Marie Defossez est né en 1971 ...</p>",
                "website": ""
            }
        ],
        "media": [
            {
                "nature": "epub",
                "key_type": "isbn13",
                "id": "immateriel.frO688313-9782889055784-epub",
                "key": "9782889055784",
                "issued_on": "2019-04-30T06:00:00+02:00",
                "current_holds": 0
            },
            {
                "nature": "paper",
                "key_type": "isbn13",
                "id": "immateriel.frO688313-9782889119714-paper",
                "key": "9782889119714",
                "issued_on": None,
                "current_holds": 0
            }
        ],
        "id": "immateriel.frO688313",
        "link": "http://mediatheque-valais.cantookstation.eu/resources/" +
                "5b18c6bc235794540e2cbe72",
        "created_at": "2018-06-07T07:46:36+02:00",
        "updated_at": "2019-04-21T07:47:19+02:00",
        "publisher_name": "Jouvence",
        "classifications": [
            {
                "standard": "bisac",
                "identifiers": [
                    "SEL000000"
                ],
                "captions": [
                    {
                        "fr": None,
                        "en": None
                    }
                ]
            },
            {
                "standard": "cantook",
                "identifiers": [
                    "self-help",
                    "health"
                ],
                "captions": [
                    {
                        "fr": "Croissance personnelle",
                        "en": "Self-Help"
                    },
                    {
                        "fr": "Santé",
                        "en": "Health"
                    }
                ]
            },
            {
                "standard": "feedbooks",
                "identifiers": [
                    "FBSEL000000",
                    "FBHEA014000",
                    "FBNFC000000",
                    "FBHEA000000"
                ],
                "captions": [
                    {
                        "fr": "Développement Personnel",
                        "en": "Self-help"
                    },
                    {
                        "fr": "Bien-être",
                        "en": "Well being"
                    },
                    {
                        "fr": "Documentaires",
                        "en": "Non-Fiction"
                    },
                    {
                        "fr": "Santé & Vie quotidienne",
                        "en": "Health & fitness"
                    }
                ]
            }
        ],
        "publisher": {
            "name": "Jouvence"
        }
    }

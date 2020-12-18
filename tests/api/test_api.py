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

"""Test Ebook api."""

from copy import deepcopy

from rero_ebooks.api import Ebook
from rero_ebooks.minters import build_ebook_pid


def test_merge_and_remove_uri_records(es, db, cdf_record, mv_record):
    """Test merge ebook records."""
    cover = "http://images.immateriel.fr/covers/X8WRJB3.png"

    cdf = 'http://la-chaux-de-fonds.ebibliomedia.ch/resources/'\
          '5788be89dde6b2d458f42b35'

    mv = 'http://mediatheque-valais.ebibliomedia.ch/resources/'\
         '5788be89dde6b2d458f42b35'

    orig_mv_record = deepcopy(mv_record)
    orig_cdf_record = deepcopy(cdf_record)

    cdf_record_pid = build_ebook_pid(cdf_record, 'cantook')
    cdf_record_exists = Ebook.get_record_by_pid(cdf_record_pid)
    assert cdf_record_exists is None
    new_cdf_record, cdf_status = Ebook.create_or_update(
        cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert cdf_status == 'CREATE'
    assert new_cdf_record['electronic_location_and_access'][0][
        'uniform_resource_identifier'
    ]
    merged_record, merged_record_status = Ebook.create_or_update(
        mv_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert merged_record_status == 'UPDATE'
    ela = merged_record['electronic_location_and_access']
    assert len(ela) == 3
    assert mv == ela[0]['uniform_resource_identifier']
    assert cover == ela[1]['uniform_resource_identifier']
    assert cdf == ela[2]['uniform_resource_identifier']

    removed_uri_record, removed_uri_record_status = Ebook.remove_uri(
        orig_mv_record,
        vendor='cantook',
        url='http://mediatheque-valais.ebibliomedia.ch',
        dbcommit=True,
        reindex=True
    )
    ela = removed_uri_record['electronic_location_and_access']
    assert len(ela) == 2
    assert removed_uri_record_status == 'REMOVE URIs: 1'
    assert cover == ela[0]['uniform_resource_identifier']
    assert cdf == ela[1]['uniform_resource_identifier']

    removed_uri_record, removed_uri_record_status = Ebook.remove_uri(
        orig_cdf_record,
        vendor='cantook',
        url='http://la-chaux-de-fonds.ebibliomedia.ch',
        dbcommit=True,
        reindex=True
    )
    ela = removed_uri_record['electronic_location_and_access']
    assert len(ela) == 1
    assert removed_uri_record_status == 'REMOVE URIs: 1'
    assert cover == ela[0]['uniform_resource_identifier']


def test_merge_records_same(es, db, cdf_record, dojson_like_cdf_record):
    """Test merge ebook records."""
    cdf_record_pid = build_ebook_pid(cdf_record, 'cantook')
    new_cdf_record, cdf_status = Ebook.create_or_update(
        cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    merged_record, merged_record_status = Ebook.create_or_update(
        dojson_like_cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert merged_record_status == 'UPDATE'
    ela = merged_record['electronic_location_and_access']
    assert len(ela) == 2


def test_create_or_update_record(db, cdf_record):
    """Test create record."""
    record = Ebook.get_record_by_pid('cantook-5788be89dde6b2d458f42b35')
    assert record is None
    new_record, status = Ebook.create_or_update(
        cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert status == 'CREATE'
    record = Ebook.get_record_by_pid('cantook-5788be89dde6b2d458f42b35')
    assert record['pid'] == 'cantook-5788be89dde6b2d458f42b35'
    record['title'] = 'The Nest'
    mod_record, status = Ebook.create_or_update(
        record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert status == 'UPDATE'

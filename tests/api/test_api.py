# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test Ebook api."""

from rero_ebooks.api import Ebook
from rero_ebooks.minters import build_ebook_pid


def test_merge_records(db, cdf_record, mv_record):
    """Test merge ebook records."""
    cdf = 'http://la-chaux-de-fonds.ebibliomedia.ch/resources/'\
          '5788be89dde6b2d458f42b35'

    mv = 'http://mediatheque-valais.ebibliomedia.ch/resources/'\
         '5788be89dde6b2d458f42b35'

    cdf_record_pid = build_ebook_pid(cdf_record, 'cantook')
    cdf_record_exists = Ebook.get_record_by_pid(cdf_record_pid)
    assert cdf_record_exists is None
    new_cdf_record, cdf_status = Ebook.create_or_update(
        cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert cdf_status == 'created'
    assert new_cdf_record['electronic_location_and_access'][0][
        'uniform_resource_identifier'
    ]
    merged_record, merged_record_status = Ebook.create_or_update(
        mv_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert merged_record_status == 'updated'
    ela = merged_record['electronic_location_and_access']
    assert len(ela) == 2
    first_uri = ela[0]['uniform_resource_identifier'][0]
    second_uri = ela[1]['uniform_resource_identifier'][0]
    assert mv == first_uri
    assert cdf == second_uri


def test_merge_records_same(db, cdf_record, dojson_like_cdf_record):
    """Test merge ebook records."""
    cdf_record_pid = build_ebook_pid(cdf_record, 'cantook')
    new_cdf_record, cdf_status = Ebook.create_or_update(
        cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    merged_record, merged_record_status = Ebook.create_or_update(
        dojson_like_cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert merged_record_status == 'updated'
    ela = merged_record['electronic_location_and_access']
    assert len(ela) == 1


def test_create_or_update_record(db, cdf_record):
    """Test create record."""
    record = Ebook.get_record_by_pid('cantook-5788be89dde6b2d458f42b35')
    assert record is None
    new_record, status = Ebook.create_or_update(
        cdf_record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert status == 'created'
    record = Ebook.get_record_by_pid('cantook-5788be89dde6b2d458f42b35')
    assert record['pid'] == 'cantook-5788be89dde6b2d458f42b35'
    record['title'] = 'The Nest'
    mod_record, status = Ebook.create_or_update(
        record, vendor='cantook', dbcommit=True, reindex=True
    )
    assert status == 'updated'

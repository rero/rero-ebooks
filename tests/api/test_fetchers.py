# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test minters and providers."""

from uuid import uuid4

from rero_ebooks.fetchers import ebook_pid_fetcher
from rero_ebooks.minters import ebook_pid_minter


def test_item_id_fetcher(base_app, db):
    """Test fetcher."""
    data = {
        'other_standard_identifier': [{
            'standard_number_or_code':
                'http://cantookstation.com/resources/55373535cdd23087a9789b72'
        }]
    }
    # first record
    rec_uuid = uuid4()
    ebook_pid_minter(rec_uuid, data)
    fetched_pid = ebook_pid_fetcher(rec_uuid, data)
    assert fetched_pid.pid_type == fetched_pid.provider.pid_type
    assert fetched_pid.pid_type == 'ebook'
    assert fetched_pid.pid_value == '55373535cdd23087a9789b72'

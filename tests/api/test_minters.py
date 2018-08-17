# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test minters and providers."""

from uuid import uuid4

from rero_ebooks.minters import ebook_pid_minter


def test_ebook_id_minter(base_app, db):
    """Test minter."""
    data = {
        'other_standard_identifier': [{
            'standard_number_or_code':
                'http://cantookstation.com/resources/55373535cdd23087a9789b72'
        }]
    }
    # first record
    rec_uuid = uuid4()
    ebook_pid_minter(rec_uuid, data, 'cantook')
    assert data.get('pid') == 'cantook-55373535cdd23087a9789b72'

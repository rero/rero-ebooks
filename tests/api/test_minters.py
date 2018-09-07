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

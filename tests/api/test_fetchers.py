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

"""Test minters and providers."""

from uuid import uuid4

from rero_ebooks.fetchers import ebook_pid_fetcher
from rero_ebooks.minters import ebook_pid_minter


def test_item_id_fetcher(base_app, db):
    """Test fetcher."""
    data = {
        "other_standard_identifier": [
            {
                "standard_number_or_code": "http://cantookstation.com/resources/55373535cdd23087a9789b72"
            }
        ]
    }
    # first record
    rec_uuid = uuid4()
    ebook_pid_minter(rec_uuid, data, "cantook")
    fetched_pid = ebook_pid_fetcher(rec_uuid, data)
    assert fetched_pid.pid_type == fetched_pid.provider.pid_type
    assert fetched_pid.pid_type == "ebook"
    assert fetched_pid.pid_value == "cantook-55373535cdd23087a9789b72"

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

"""Ebooks fetchers."""

from collections import namedtuple

from .providers import EbookPidProvider

FetchedPID = namedtuple("FetchedPID", ["provider", "pid_type", "pid_value"])
"""A pid fetcher."""


def ebook_pid_fetcher(record_uuid, data, pid_key="pid"):
    """Fetch a ebook's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    return FetchedPID(
        provider=EbookPidProvider,
        pid_type=EbookPidProvider.pid_type,
        pid_value=str(data[pid_key]),
    )

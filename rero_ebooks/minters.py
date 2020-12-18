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

"""Ebooks minters."""

from invenio_oaiserver.minters import oaiid_minter

from .providers import EbookPidProvider


def build_ebook_pid(data, source):
    """Build ebook pid from record."""
    assert 'other_standard_identifier' in data
    assert (
        'standard_number_or_code'
        in data.get('other_standard_identifier')[0]
    )

    pid_value = (
        data.get('other_standard_identifier')[0]
        .get('standard_number_or_code')
        .split('/')[-1]
    )
    return source + '-' + pid_value


def ebook_pid_minter(record_uuid, data, source, pid_key='pid',
                     object_type='rec'):
    """Mint record identifiers.

    This is a minter specific for ebooks.
    With the help of
    :class:`rero_ebooks.providers.EbookPidProvider`, it creates
    the PID instance with `rec` as predefined `object_type`.
    Procedure followed: (we will use `control_number` as value of
    `PIDSTORE_RECID_FIELD` for the simplicity of the documentation.)
    #. If a `pid` field is already there, a `AssertionError`
    exception is raised.
    #. The provider is initialized with the help of
    :class:`rero_ebooks.providers.EbookPidProvider`.
    It's called with default value 'rec' for `object_type` and `record_uuid`
    variable for `object_uuid`.
    #. The new `id_value` is stored inside `data` as `pid` field.
    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A fresh `invenio_pidstore.models.PersistentIdentifier` instance.
    """
    assert pid_key not in data
    pid_value = build_ebook_pid(data, source)
    provider = EbookPidProvider.create(
        object_type='rec', pid_value=pid_value, object_uuid=record_uuid)
    data[pid_key] = pid_value
    oaiid_minter(record_uuid, data)
    return provider.pid

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

"""Ebooks minters."""

from flask import current_app
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


def ebook_pid_minter(record_uuid, data, source):
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
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    assert pid_field not in data
    pid_value = build_ebook_pid(data, source)
    provider = EbookPidProvider.create(
        object_type='rec', pid_value=pid_value, object_uuid=record_uuid)
    data[pid_field] = pid_value
    oaiid_minter(record_uuid, data)
    return provider.pid

# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Ebooks minters."""

from flask import current_app
from invenio_oaiserver.minters import oaiid_minter

from .providers import EbookPidProvider


def ebook_pid_minter(record_uuid, data):
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
    assert 'other_standard_identifier' in data
    assert 'standard_number_or_code' in \
        data.get('other_standard_identifier')[0]

    pid_value = data.get('other_standard_identifier')[0]\
                    .get('standard_number_or_code').split('/')[-1]
    provider = EbookPidProvider.create(
        object_type='rec', pid_value=pid_value, object_uuid=record_uuid)
    data[pid_field] = pid_value
    oaiid_minter(record_uuid, data)
    return provider.pid

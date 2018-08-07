# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Ebooks fetchers."""

from collections import namedtuple

from flask import current_app

from .providers import EbookPidProvider

FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])
"""A pid fetcher."""


def ebook_pid_fetcher(record_uuid, data):
    """Fetch a ebook's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    return FetchedPID(
        provider=EbookPidProvider,
        pid_type=EbookPidProvider.pid_type,
        pid_value=str(data[pid_field]),
    )

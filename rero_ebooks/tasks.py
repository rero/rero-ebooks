# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks to create records."""

from __future__ import absolute_import, print_function

import click
from celery import shared_task
from invenio_oaiharvester.api import list_records
from invenio_oaiharvester.signals import oaiharvest_finished

from .api import Ebook


@shared_task(ignore_result=True)
def create_records(records, verbose=False):
    """Records creation and indexing."""
    for record in records:
        rec, status = Ebook.create_or_update(
            record,
            # TODO vendor config
            vendor='cantook',
            dbcommit=True,
            reindex=True
        )
        if verbose:
            click.echo('record uuid: ' + str(rec.id) + ' | ' + status)
        # TODO bulk update and reindexing


@shared_task(ignore_result=True)
def harvest(source, verbose=False):
    """Async source harvesting."""
    records = None
    request, records = list_records(
        name=source
    )
    if records:
        oaiharvest_finished.send(
            request,
            records=records,
            name=source,
            verbose=verbose
        )

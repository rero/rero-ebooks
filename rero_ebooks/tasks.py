# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks to create records."""

from __future__ import absolute_import, print_function

from celery import shared_task
from flask import current_app

from .api import Ebook


@shared_task(ignore_result=True)
def create_records(records):
    """Records creation and indexing."""
    for record in records:
        rec, status = Ebook.create_or_update(
            record,
            # TODO vendor config
            vendor='cantook',
            dbcommit=True,
            reindex=True
        )
        current_app.logger.info(
            'record uuid: {0} | {1}'.format(rec.id, status)
        )
        # TODO bulk update and reindexing
    current_app.logger.info(
        'records updated: {0}'.format(len(records))
    )
    return len(records)


@shared_task(ignore_result=True)
def delete_records(records):
    """Records deletion and indexing."""
    for record in records:
        status = Ebook.delete(
            record,
            vendor='cantook'
        )
        current_app.logger.info(
            'record: {0} | DELETED {1}'.format(record, status)
        )
        # TODO bulk update and reindexing
    current_app.logger.info(
        'records deleted: {0}'.format(len(records))
    )
    return len(records)

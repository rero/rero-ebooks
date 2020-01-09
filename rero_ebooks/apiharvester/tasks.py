# -*- coding: utf-8 -*-
#
# This file is part of RERO EBOOKS.
# Copyright (C) 2017 RERO.
#
# RERO EBOOKS is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# RERO EBOOKS is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RERO EBOOKS; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""ApiHarvester tasks."""

from __future__ import absolute_import, print_function

import click
from celery import shared_task
from flask import current_app
from invenio_records_rest.utils import obj_or_import_string

from .utils import get_apiharvest_object


@shared_task(ignore_result=True, soft_time_limit=3600)
def harvest_records(name, from_date=None, max=0, verbose=False):
    """Harvest records."""
    count = -1

    config = get_apiharvest_object(name=name)
    if config:
        if not from_date:
            from_date = config.lastrun.isoformat()
        msg = 'API harvest {name} class name: {classname} '.format(
            name=name,
            classname=config.classname
        )
        msg += 'from date: {from_date} url: {url}'.format(
            from_date=from_date,
            url=config.url
        )
        current_app.logger.info(msg)
        HarvestClass = obj_or_import_string(config.classname)
        harvest = HarvestClass(config=config, verbose=verbose)
        config.update_lastrun()
        total = harvest.get_records(
            from_date=from_date,
            max=max
        )
        msg = ('API harvest items={total} available={count_available} |'
               ' got={count} new={count_new} updated={count_upd}'
               ' deleted={count_del}'
               ' from {name}.').format(
            total=total,
            count_available=harvest.count_available,
            count=harvest.count,
            count_new=harvest.count_new,
            count_upd=harvest.count_upd,
            count_del=harvest.count_del,
            name=name
        )
        if verbose:
            click.echo(msg)
        current_app.logger.info(msg)
        count = harvest.count
    else:
        current_app.logger.error('No config found: {name}'.format(
            name=name
        ))
    return count

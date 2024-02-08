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

    if config := get_apiharvest_object(name=name):
        if not from_date:
            from_date = config.lastrun.isoformat()
        msg = f"API harvest {name} class name: {config.classname} "
        msg += f"from date: {from_date} url: {config.url}"

        current_app.logger.info(msg)
        HarvestClass = obj_or_import_string(config.classname)
        harvest = HarvestClass(config=config, verbose=verbose)
        config.update_lastrun()
        total = harvest.get_records(from_date=from_date, max=max)
        msg = (
            f"API harvest items={total} available={harvest.count_available} |"
            f" got={harvest.count} new={harvest.count_new}"
            f" updated={harvest.count_upd} deleted={harvest.count_del}"
            f" from {name}."
        )
        if verbose:
            click.echo(msg)
        current_app.logger.info(msg)
        count = harvest.count
    else:
        current_app.logger.error(f"No config found: {name}")
    return count

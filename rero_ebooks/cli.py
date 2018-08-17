# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Click command-line interface for ebook record management."""

from __future__ import absolute_import, print_function

import json
import sys

import click
from flask.cli import with_appcontext
from invenio_records.cli import records

from rero_ebooks.api import Ebook


@records.command()
@click.argument('source', type=click.File('r'), default=sys.stdin)
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option('-s', '--vendor', 'vendor', default='cantook')
@with_appcontext
def create_or_update(source, verbose, vendor):
    """Create or update ebook records."""
    click.secho('Create or update book records:', fg='green')
    data = json.load(source)

    if isinstance(data, dict):
        data = [data]

    for record in data:
        record, status = Ebook.create_or_update(
            record, vendor=vendor, dbcommit=True, reindex=True
        )
        click.echo('record uuid: ' + str(record.id) + '| ' + status)

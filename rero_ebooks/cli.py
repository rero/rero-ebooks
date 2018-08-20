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
import yaml
from flask.cli import with_appcontext
from invenio_oaiharvester.cli import oaiharvester
from invenio_records.cli import records

from .api import Ebook
from .utils import add_oai_source


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


@oaiharvester.command('addsource')
@click.argument('name')
@click.argument('baseurl')
@click.option('-m', '--metadataprefix', default='marc21',
              help='The prefix for the metadata')
@click.option('-s', '--setspecs', default='',
              help='The ‘set’ criteria for the harvesting')
@click.option('-c', '--comment', default='',
              help='Comment')
@with_appcontext
def add_oai_source_config(name, baseurl, metadataprefix, setspecs, comment):
    """Add OAIHarvestConfig."""
    click.echo('Add OAIHarvestConfig: {0} '.format(name), nl=False)
    add_oai_source(
        name=name,
        baseurl=baseurl,
        metadataprefix=metadataprefix,
        setspecs=setspecs,
        comment=comment
    )
    click.secho('Ok', fg='green')


@oaiharvester.command('initconfig')
@click.argument('configfile', type=click.File('rb'))
@with_appcontext
def init_oai_harvest_config(configfile):
    """Init OAIHarvestConfig."""
    configs = yaml.load(configfile)
    for name, values in sorted(configs.items()):
        baseurl = values['baseurl']
        metadataprefix = values.get('metadataprefix', 'marc21')
        setspecs = values.get('setspecs', '')
        comment = values.get('comment', '')
        click.echo(
            'Add OAIHarvestConfig: {0} {1} '.format(name, baseurl), nl=False
        )
        add_oai_source(
            name=name,
            baseurl=baseurl,
            metadataprefix=metadataprefix,
            setspecs=setspecs,
            comment=comment
        )
        click.secho('Ok', fg='green')

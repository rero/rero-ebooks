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

"""Click command-line interface for mef person management."""

from __future__ import absolute_import, print_function

import click
import yaml
from dateutil import parser
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.local import LocalProxy

from rero_ebooks.apiharvester.tasks import harvest_records

from .models import ApiHarvestConfig
from .utils import api_source

datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


@click.group()
def apiharvester():
    """Api harvester commands."""


@apiharvester.command('source')
@click.argument('name')
@click.option('-U', '--url', default='', help='Url')
@click.option('-n', '--classname', default='', help='Class name')
@click.option('-c', '--code', default='', help='Code')
@click.option(
    '-u', '--update', is_flag=True, default=False, help='Update config'
)
@with_appcontext
def api_source_config(name, url, classname, code, update):
    """Add or Update ApiHarvestConfig."""
    msg = api_source(
        name=name,
        url=url,
        classname=classname,
        code=code,
        update=update
    )
    click.echo(
        '{msg} ApiHarvestConfig: {name}'.format(
            msg=msg,
            name=name
        )
    )


@apiharvester.command('sources')
@click.argument('configfile', type=click.File('rb'))
@click.option(
    '-u', '--update', is_flag=True, default=False, help='Update config'
)
@with_appcontext
def api_source_config_from_file(configfile, update):
    """Add or update ApiHarvestConfigs from file."""
    configs = yaml.load(configfile, Loader=yaml.FullLoader)
    if configs:
        for name, values in sorted(configs.items()):
            url = values.get('url', '')
            classname = values.get('classname', '')
            code = values.get('code', '')
            msg = api_source(
                name=name,
                url=url,
                classname=classname,
                code=code,
                update=update
            )
            click.echo(
                '{msg} ApiHarvestConfig: {name}'.format(
                    msg=msg,
                    name=name
                )
            )

    else:
        click.secho(
            'ERROR: no YML config found in: {filename}'.format(
                filename=configfile.name
            )
        )


@apiharvester.command('harvest')
@click.option('-n', '--name', default=None,
              help='Name of persistent configuration to use.')
@click.option('-f', '--from-date', default=None,
              help='The lower bound date for the harvesting (optional).')
@click.option('-k', '--enqueue', is_flag=True, default=False,
              help='Enqueue harvesting and return immediately.')
@click.option('-m', '--max', type=int, default=0,
              help='maximum of records to harvest (optional).')
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@with_appcontext
def harvest(name, from_date, enqueue, max, verbose):
    """Harvest records from an API repository."""
    if name:
        click.secho('Harvest api: {name}'.format(name=name), fg='green')
    if from_date:
        from_date = parser.parse(from_date).isoformat()
    if enqueue:
        async_id = harvest_records.delay(name=name, from_date=from_date,
                                         max=max, verbose=verbose)
        if verbose:
            click.echo('AsyncResult {id}'.format(id=async_id))
    else:
        harvest_records(name=name, from_date=from_date,
                        max=max, verbose=verbose)


@apiharvester.command('info')
@with_appcontext
def info():
    """List infos for tasks."""
    apis = ApiHarvestConfig.query.all()
    for api in apis:
        click.echo(api.name)
        click.echo('\tlastrun   : {lastrun}'.format(lastrun=api.lastrun))
        click.echo('\turl       : {url}'.format(url=api.url))
        click.echo('\tclassname : {classname}'.format(classname=api.classname))
        click.echo('\tcode   : {code}'.format(code=api.code))

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

"""Click command-line interface for ebooks apiharvester."""

from __future__ import absolute_import, print_function

import click
import yaml
from dateutil import parser
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.local import LocalProxy

from rero_ebooks.apiharvester.tasks import harvest_records

from .models import ApiHarvestConfig
from .utils import add_set, api_source

datastore = LocalProxy(lambda: current_app.extensions["security"].datastore)


@click.group()
def apiharvester():
    """Api harvester commands."""


@apiharvester.command("source")
@click.argument("name")
@click.option("-U", "--url", default="", help="Url")
@click.option("-n", "--classname", default="", help="Class name")
@click.option("-c", "--code", default="", help="Code")
@click.option("-u", "--update", is_flag=True, default=False, help="Update config")
@with_appcontext
def api_source_config(name, url, classname, code, update):
    """Add or Update ApiHarvestConfig."""
    msg = api_source(name=name, url=url, classname=classname, code=code, update=update)
    click.echo(f"{msg} ApiHarvestConfig: {name}")


@apiharvester.command("sources")
@click.argument("configfile", type=click.File("rb"))
@click.option("-u", "--update", is_flag=True, default=False, help="Update config")
@with_appcontext
def api_source_config_from_file(configfile, update):
    """Add or update ApiHarvestConfigs from file."""
    if configs := yaml.load(configfile, Loader=yaml.FullLoader):
        for name, values in sorted(configs.items()):
            url = values.get("url", "")
            classname = values.get("classname", "")
            code = values.get("code", "")
            msg = api_source(
                name=name, url=url, classname=classname, code=code, update=update
            )
            click.echo(f"{msg} ApiHarvestConfig: {name}")

    else:
        click.secho(f"ERROR: no YML config found in: {configfile.name}")


@apiharvester.command("initsets")
@click.argument("configfile", type=click.File("rb"))
@click.option("-v", "--verbose", "verbose", is_flag=True, default=False)
@with_appcontext
def init_oai_sets(configfile, verbose):
    """Init OAIsets."""
    configs = yaml.load(configfile, Loader=yaml.FullLoader)
    for name, values in sorted(configs.items()):
        description = values.get("description", "...")
        pattern = values["pattern"]
        msg = add_set(spec=name, name=name, description=description, pattern=pattern)
        if verbose:
            click.echo(msg)


@apiharvester.command("harvest")
@click.option(
    "-n", "--name", default=None, help="Name of persistent configuration to use."
)
@click.option(
    "-f",
    "--from-date",
    default=None,
    help="The lower bound date for the harvesting (optional).",
)
@click.option(
    "-k",
    "--enqueue",
    is_flag=True,
    default=False,
    help="Enqueue harvesting and return immediately.",
)
@click.option(
    "-m", "--max", type=int, default=0, help="maximum of records to harvest (optional)."
)
@click.option("-v", "--verbose", "verbose", is_flag=True, default=False)
@with_appcontext
def harvest(name, from_date, enqueue, max, verbose):
    """Harvest records from an API repository."""
    if name:
        click.secho(f"Harvest api: {name}", fg="green")
    if from_date:
        from_date = parser.parse(from_date).isoformat()
    if enqueue:
        async_id = harvest_records.delay(
            name=name, from_date=from_date, max=max, verbose=verbose
        )
        if verbose:
            click.echo(f"AsyncResult {async_id}")
    else:
        harvest_records(name=name, from_date=from_date, max=max, verbose=verbose)


@apiharvester.command("info")
@with_appcontext
def info():
    """List infos for tasks."""
    apis = ApiHarvestConfig.query.all()
    for api in apis:
        click.echo(api.name)
        click.echo(f"\tlastrun   : {api.lastrun}")
        click.echo(f"\turl       : {api.url}")
        click.echo(f"\tclassname : {api.classname}")
        click.echo(f"\tcode   : {api.code}")

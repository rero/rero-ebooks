# -*- coding: utf-8 -*-
#
# This file is part of RERO Ebooks.
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# RERO Ebooks is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RERO Ebooks; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Test Api CLI."""

from __future__ import absolute_import, print_function

import os
import re

import pytest
import responses
from click.testing import CliRunner
from flask.cli import ScriptInfo

from rero_ebooks.apiharvester import cli

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )


def test_config(app, apiharvester_config_vs):
    """Test config cli."""
    runner = CliRunner()
    script_info = ScriptInfo(create_app=lambda info: app)

    res = runner.invoke(cli.info, obj=script_info)
    assert 0 == res.exit_code
    assert res.output == ''

    res = runner.invoke(
        cli.api_source_config,
        [
            'VS',
            '-U', apiharvester_config_vs['url'],
            '-n', apiharvester_config_vs['classname'],
            '-c', apiharvester_config_vs['code'],
            '-u'
        ],
        obj=script_info
    )
    assert 0 == res.exit_code
    assert res.output == 'Add ApiHarvestConfig: VS\n'
    config_nj_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../data/apisource-nj.yml',
    )
    res = runner.invoke(
        cli.api_source_config_from_file,
        [
            config_nj_filename,
            '-u'
        ],
        obj=script_info
    )
    assert 0 == res.exit_code
    assert res.output == 'Add ApiHarvestConfig: NJ\n'


@pytest.mark.skip(
    reason="Have to wait for response to implement re.compile for add_passthru"
)
@responses.activate
def test_harvest(app, apiharvester_config_vs, apiharvester_apiresponse_vs):
    """Test harvest cli."""
    runner = CliRunner()
    script_info = ScriptInfo(create_app=lambda info: app)

    """Mock a request response."""
    responses.add_passthru(
        re.compile('http://localhost:9200/(.*)')
    )
    url1 = '{url}{static}'.format(
        url=apiharvester_config_vs.get('url'),
        static='/v1/resources.json?start_at=1900-01-01T00:00:00&page=1',
    )
    headers1 = {
        'X-Total-Pages': '1',
        'X-Total-Items': '1',
        'X-Per-Page': '20',
        'X-Current-Page': '1'
    }
    responses.add(
        responses.GET,
        url1,
        status=200,
        json=apiharvester_apiresponse_vs,
        headers=headers1
    )
    url2 = '{url}{static}'.format(
        url=apiharvester_config_vs.get('url'),
        static='/v1/resources.json?start_at=1900-01-01T00:00:00&page=2'
    )
    headers2 = {
        'X-Total-Pages': '1',
        'X-Total-Items': '1',
        'X-Per-Page': '20',
        'X-Current-Page': '2'
    }
    responses.add(
        responses.GET,
        url2,
        status=200,
        headers=headers2
    )

    res = runner.invoke(
        cli.harvest,
        [
            '-n', 'VS', '-v'
        ],
        obj=script_info
    )
    assert 0 == res.exit_code
    output = '{line1}\n{line2}\n{line3}\n{line4}\n'.format(
        line1='Harvest api: VS',
        line2=('API page: 1 url: {url}').format(url=url1),
        line3='1: {link}'.format(
            link=apiharvester_apiresponse_vs['resources'][0]['link']
        ),
        line4='API harvest 1 items | got 1 from VS'
    )
    assert res.output == output

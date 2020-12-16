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

"""ApiHarvester utils."""

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_db import db
from invenio_oaiserver.models import OAISet
from sqlalchemy.exc import OperationalError

from .errors import ApiHarvesterConfigNotFound
from .models import ApiHarvestConfig


def add_set(spec, name, pattern, description='...'):
    """Add OAI set.

    :param spec: set identifier
    :param name: human readable name of the set
    :param pattern: search pattern to get records
    :param description: human readable description
    """
    try:
        oaiset = OAISet(spec=spec, name=name, description=description)
        oaiset.search_pattern = pattern
        db.session.add(oaiset)
        db.session.commit()
        msg = 'OAIset added: {name}'.format(name=name)
    except Exception as err:
        db.session.rollback()
        msg = 'OAIset exist: {name}'.format(name=name)
    return msg


def api_source(name, url='', classname=None, code='', update=False):
    """Add ApiHarvestConfig do DB.

    name: name for the configuaration
    url: harvesting url
    classname: Class responsible for geting record_serializers
    code: code added to electronic_location['nonpublic_note']
    update: update configuration if exist
    """
    with current_app.app_context():
        msg = 'No Update'
        source = ApiHarvestConfig.query.filter_by(name=name).first()
        if not source:
            source = ApiHarvestConfig(
                name=name,
                url=url,
                classname=classname,
                code=code
            )
            source.save()
            db.session.commit()
            msg = 'Add'
        elif update:
            source.name = name
            msg = []
            if url != '':
                source.url = url
                msg.append('url:{}'.format(url))
            if classname != '':
                source.classname = classname
                msg.append('classname:{}'.format(classname))
            if code != '':
                source.code = code
                msg.append('code:{}'.format(code))
            db.session.commit()
            msg = 'Update {}'.format(', '.join(msg))
        return msg


def get_apiharvest_object(name):
    """Query and returns an ApiHarvestConfig object based on its name.

    :param name: The name of the ApiHarvestConfig object.
    :return: The ApiHarvestConfig object.
    """
    get_config_error_count = 0
    get_config_ok = False
    while not get_config_ok and get_config_error_count < 5:
        try:
            obj = ApiHarvestConfig.query.filter_by(name=name).first()
            get_config_ok = True
        except OperationalError:
            get_config_error_count += 1
            msg = 'ApiHarvestConfig OperationalError: {count} {name}'.format(
                count=get_config_error_count,
                name=name
            )
            current_app.logger.error(msg)

    if not obj:
        raise ApiHarvesterConfigNotFound(
            'Unable to find ApiHarvesterConfig obj with name %s.'
            % name
        )

    return obj

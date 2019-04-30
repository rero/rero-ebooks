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

from .models import ApiHarvestConfig


def api_source(name, url='', classname=None, code='', update=False):
    """Add ApiHarvestConfig do DB.

    name: name for the configuaration
    url: harvesting url
    classname: Class responsible for geting record_serializers
    code: code added to electronic_location['nonpublic_note']
    update: update configuration if exist
    """
    with current_app.app_context():
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
            return 'Add'
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
            return 'Update {}'.format(', '.join(msg))
        return 'No Update'

# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utilities."""


from flask import current_app
from invenio_db import db
from invenio_oaiharvester.models import OAIHarvestConfig


def add_oai_source(name, baseurl, metadataprefix='marc21',
                   setspecs='', comment=''):
    """Add OAIHarvestConfig."""
    with current_app.app_context():
        if OAIHarvestConfig.query.filter_by(name=name).count() == 0:
            source = OAIHarvestConfig(
                name=name,
                baseurl=baseurl,
                metadataprefix=metadataprefix,
                setspecs=setspecs,
                comment=comment
            )
            source.save()
            db.session.commit()
            return True
        else:
            return False

# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""RERO DOC Invenio application."""


from invenio_oaiharvester.signals import oaiharvest_finished

from . import config
from .receivers import publish_harvested_records


class ReroEBooks(object):
    """ReroEBooks App extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)
        self.register_signals(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['reroebooks-app'] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('REROEBOOKS_APP_'):
                app.config.setdefault(k, getattr(config, k))

    @staticmethod
    def register_signals(app):
        """Register Zenodo Deposit signals."""
        oaiharvest_finished.connect(publish_harvested_records,
                                    weak=False)

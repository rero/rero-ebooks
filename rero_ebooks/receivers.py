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

"""Signals connections for RERO ebooks."""

from dojson.contrib.marc21.utils import create_record

from rero_ebooks.tasks import create_records

from .dojson.marc21 import marc21


def publish_harvested_records(sender=None, records=[], *args, **kwargs):
    """Create, index the harvested records."""
    # name = kwargs['name']
    converted_records = []
    for record in records:
        rec = create_record(record.xml)
        rec = marc21.do(rec)
        converted_records.append(rec)
    verbose = kwargs.get('verbose', False)
    create_records(converted_records, verbose=verbose)

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

"""API for cantook records."""


from __future__ import absolute_import, print_function

import json

import click
from requests import codes as requests_codes
from requests import get as requests_get

from ..api import Ebook
from ..apiharvester.models import ApiHarvestConfig
from ..dojson.json import cantook_json


class ApiCantook():
    """ApiCantook class.

    Class for harvesting ebooks from cantook API resources.

    config: saved config from apiharvester class
    verbose: print verbose messages
    file: save harvested records to file default no saving
    intent: intention for saved file
    """

    def __init__(self, config, file=None, indent=None, verbose=False):
        """Class init."""
        self.config = config
        self.verbose = verbose
        self.file = file
        if self.file:
            file.write('[\n')
        self.indent = indent
        self._count = 0
        self._max = 0
        self._vendor = 'cantook'

    @classmethod
    def get_config(cls, name):
        """Get config for name."""
        return ApiHarvestConfig.query.filter_by(name=name).first()

    def get_request_url(self, start_date='1990-01-01', page=1):
        """Get request URL.

        start_date: date from where records havs to be harvested
        page: page from whre records have to be harvested
        """
        params = 'start_at={start_date}&page={page}'.format(
            start_date=start_date,
            page=page
        )
        return self.config.url + '/v1/resources.json?{params}'.format(
            params=params
        )

    def save_record(self, record):
        """Save record to file."""
        if self.file:
            json.dump(record, self.file, indent=self.indent)
            self.file.write(',\n')

    def add_nonpublic_note(self, record):
        """Add nonpublic note to electronic location and access."""
        electronic_locations = record.get('electronic_location_and_access', [])
        new_electronic_locations = []
        for electronic_location in electronic_locations:
            url = '/'.join(
                electronic_location['uniform_resource_identifier'].split(
                    '/'
                )[:3]
            )
            if url == self.config.url:
                electronic_location['nonpublic_note'] = self.config.code
            new_electronic_locations.append(electronic_location)
        return record

    def create_update_record(self, record):
        """Create new record or update record."""
        record = cantook_json.do(record)
        record = self.add_nonpublic_note(record)
        record, msg = Ebook.create_or_update(
            data=record,
            vendor=self._vendor,
            dbcommit=True,
            reindex=True
        )
        return record, msg

    def process_records(self, records):
        """Process records."""
        for record in records:
            self._count += 1
            if self._count < self._max or self._max == 0:
                self.save_record(record)
                record, msg = self.create_update_record(record)
                if self.verbose:
                    click.echo(
                        '{count}: {pid} {msg}'.format(
                            count=self._count,
                            pid=record['pid'],
                            msg=msg
                        )
                    )
            else:
                break

    def verbose_print(self, msg):
        """Print verbose message."""
        if self.verbose:
            click.echo(msg)

    def get_records(self, from_date, max=0, file=None):
        """Get cantook records.

        from_date: record changed after this date to get
        max: maxium records to fetcher
        file: to save the fetched record
        """
        self._count = 0
        self._max = max
        url = self.get_request_url(start_date=from_date, page=1)
        request = requests_get(url)
        total_pages = int(request.headers.get('X-Total-Pages', 0))
        total_items = int(request.headers.get('X-Total-Items', 0))
        # per_pages = int(request.headers.get('X-Per-Page', 0))
        current_page = int(request.headers.get('X-Current-Page', 0))
        while (request.status_code == requests_codes.ok and
               current_page <= total_pages and
               (self._count < self._max or self._max == 0)):
            self.verbose_print(
                'API page: {page} url: {url}'.format(
                    page=current_page,
                    url=url
                )
            )
            self.process_records(request.json().get('resources', []))
            # get next page and update current_page
            url = self.get_request_url(
                start_date=from_date,
                page=current_page+1
            )
            request = requests_get(url)
            current_page = int(request.headers.get('X-Current-Page', 0))
        if self.file:
            file.write(']')
        if (
            (max != 0 and self._count != max) or
            (max == 0 and total_items != self._count)
           ):
            # we had an ERROR
            raise('ERROR not all records harvested')

        return total_items, self._count

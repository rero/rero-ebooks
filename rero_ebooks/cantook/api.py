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
        self._url = self.config.url
        self._code = self.config.code
        self.verbose = verbose
        self.file = file
        if self.file:
            file.write('[\n')
        self.indent = indent
        self._count = 0
        self._count_new = 0
        self._count_upd = 0
        self._count_del = 0
        self._max = 0
        self._vendor = 'cantook'
        self._available_ids = {}

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
        return self._url + '/v1/resources.json?{params}'.format(
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
            if url == self._url:
                electronic_location['nonpublic_note'] = self._code
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

    def remove_uri(self, record):
        """Create new record or update record."""
        record = cantook_json.do(record)
        record, msg = Ebook.remove_uri(
            data=record,
            vendor=self._vendor,
            url=self._url,
            dbcommit=True,
            reindex=True
        )
        return record, msg

    def msg_text(self, pid, msg):
        """Logging message text."""
        return '{count}: {vendor}:{code} {pid} = {msg}'.format(
            vendor=self._vendor,
            code=self._code,
            count=self._count,
            pid=pid,
            msg=msg
        )

    def process_records(self, records):
        """Process records."""
        for record in records:
            self._count += 1
            if self._count < self._max or self._max == 0:
                if self._available_ids.get(record['id']):
                    self.save_record(record)
                    record, msg = self.create_update_record(record)
                    if msg == 'UPDATE':
                        self._count_upd += 1
                    else:
                        self._count_new += 1
                    if self.verbose:
                        click.echo(self.msg_text(pid=record['pid'],
                                                 msg=msg))
                else:
                    record, msg = self.remove_uri(record)
                    self._count_del += 1
                    if self.verbose:
                        click.echo(self.msg_text(pid=record['pid'],
                                                 msg=msg))
            else:
                break

    def verbose_print(self, msg):
        """Print verbose message."""
        if self.verbose:
            click.echo(msg)

    def init_available_ids(self, from_date):
        """Get all aavailable pids.

        from_date: record changed after this date to get
        """
        url = self.get_request_url(start_date=from_date, page=1)
        url += '&available=1'
        request = requests_get(url)
        total_pages = int(request.headers.get('X-Total-Pages', -1))
        total_items = int(request.headers.get('X-Total-Items', -1))
        # per_pages = int(request.headers.get('X-Per-Page', 0))
        current_page = int(request.headers.get('X-Current-Page', -1))
        count = 0
        self._available_ids = {}
        while (request.status_code == requests_codes.ok and
               current_page <= total_pages):
            self.verbose_print(
                'API page: {page} url: {url}'.format(
                    page=current_page,
                    url=url
                )
            )
            for record in request.json().get('resources', []):
                count += 1
                self._available_ids[record['id']] = count
            # get next page and update current_page
            url = self.get_request_url(
                start_date=from_date,
                page=current_page+1
            )
            url += '&available=1'
            request = requests_get(url)
            current_page = int(request.headers.get('X-Current-Page', 0))
        if total_items != count:
            # we had an ERROR
            raise ValueError('ERROR to get all available ids')
        return self._available_ids

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
        self.init_available_ids(from_date=from_date)
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
            (max != 0 and total_items >= max and self._count != max) or
            (max != 0 and total_items < max and self._count != total_items) or
            (max == 0 and total_items != self._count)
           ):
            # we had an ERROR
            raise('ERROR not all records harvested')

        return total_items

    @property
    def count(self):
        """Get count."""
        return self._count

    @property
    def count_new(self):
        """Get new count."""
        return self._count_new

    @property
    def count_upd(self):
        """Get updated count."""
        return self._count_upd

    @property
    def count_del(self):
        """Get delted count."""
        return self._count_del

    @property
    def count_available(self):
        """Get available count."""
        return len(self._available_ids)

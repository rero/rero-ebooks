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

"""API for manipulating Ebooks records."""

import copy
from uuid import uuid4

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record

from .fetchers import ebook_pid_fetcher
from .minters import build_ebook_pid, ebook_pid_minter
from .providers import EbookPidProvider


class Ebook(Record):
    """Ebook Record class."""

    minter = ebook_pid_minter
    fetcher = ebook_pid_fetcher
    provider = EbookPidProvider
    object_type = 'rec'
    uri_key = 'electronic_location_and_access'

    @classmethod
    def create_or_update(
        cls,
        data,
        id_=None,
        delete_pid=True,
        dbcommit=False,
        reindex=False,
        vendor=None,
        **kwargs
    ):
        """Create or update ebook record."""
        pid = build_ebook_pid(data, vendor)
        record = cls.get_record_by_pid(pid, with_deleted=False)
        if record:
            merged_data = cls._merge_uri(data, record)
            # TODO: merge metadata
            record.update(merged_data, dbcommit=dbcommit, reindex=reindex)
            return record, 'updated'
        else:
            created_record = cls.create(
                data,
                id_=None,
                vendor=vendor,
                delete_pid=True,
                dbcommit=dbcommit,
                reindex=reindex,
            )
            return created_record, 'created'

    @classmethod
    def create(
        cls,
        data,
        id_=None,
        delete_pid=True,
        dbcommit=False,
        reindex=False,
        vendor=None,
        **kwargs
    ):
        """Create a new ebook record."""
        assert cls.minter
        assert not data.get('pid')
        if not id_:
            id_ = uuid4()
        cls.minter(id_, data, vendor)
        record = super(Ebook, cls).create(data=data, id_=id_, **kwargs)
        if dbcommit:
            record.dbcommit(reindex)
        return record

    @classmethod
    def get_record_by_pid(cls, pid, with_deleted=False):
        """Get ebook record by pid value."""
        assert cls.provider
        resolver = Resolver(
            pid_type=cls.provider.pid_type,
            object_type=cls.object_type,
            getter=cls.get_record,
        )
        try:
            persistent_identifier, record = resolver.resolve(str(pid))
            return super(Ebook, cls).get_record(
                persistent_identifier.object_uuid, with_deleted=with_deleted
            )
        except PIDDoesNotExistError:
            return None

    @classmethod
    def _merge_uri(cls, new_record, old_record):
        """Merge new and old records."""
        field = cls.uri_key
        new_e_res = new_record.get(field)
        old_e_res = old_record.get(field)
        for e_res in old_e_res:
            # check if already exists!
            if e_res not in new_e_res:
                new_e_res.append(copy.deepcopy(e_res))
                new_record['__order__'].insert(
                    new_record['__order__'].index(field), field
                )
        return new_record

    def update(self, data, dbcommit=False, reindex=False):
        """Update data for record."""
        super(Ebook, self).update(data)
        super(Ebook, self).commit()
        if dbcommit:
            self.dbcommit(reindex)
        return self

    def dbcommit(self, reindex=False, forceindex=False):
        """Commit changes to db."""
        db.session.commit()
        if reindex:
            self.reindex(forceindex=forceindex)

    def reindex(self, forceindex=False):
        """Reindex record."""
        if forceindex:
            RecordIndexer(version_type="external_gte").index(self)
        else:
            RecordIndexer().index(self)

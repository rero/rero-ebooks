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

"""API for manipulating Ebooks records."""

import copy
from uuid import uuid4

from elasticsearch.exceptions import NotFoundError
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records.api import Record
from invenio_search.api import RecordsSearch
from sqlalchemy.orm.exc import NoResultFound

from .fetchers import ebook_pid_fetcher
from .minters import build_ebook_pid, ebook_pid_minter
from .providers import EbookPidProvider


class EbookError:
    """Base class for errors in the Ebook class."""

    class PidMissing(Exception):
        """Ebook pid missing."""


class EbooksSearch(RecordsSearch):
    """EbooksSearch."""

    class Meta:
        """Search only on documents index."""

        index = 'ebooks'
        doc_types = None
        fields = ('*', )
        facets = {}

        default_filter = None


class Ebook(Record):
    """Ebook Record class."""

    minter = ebook_pid_minter
    fetcher = ebook_pid_fetcher
    provider = EbookPidProvider
    object_type = 'rec'
    uri_key = 'electronic_location_and_access'

    @classmethod
    def _merge_uri(cls, new_record, old_record):
        """Merge new and old records."""
        field = cls.uri_key
        new_e_res = new_record.get(field)
        # change all tuples to lists
        # the dojson produces tuples and we have lists in the record
        for e_res in new_e_res:
            for key, value in e_res.items():
                if isinstance(value, tuple):
                    e_res[key] = list(value)

        old_e_res = old_record.get(field)
        for e_res in old_e_res:
            # check if already exists!
            if e_res not in new_e_res:
                new_e_res.append(copy.deepcopy(e_res))
                idx = new_record['__order__'].index(field)
                new_record['__order__'].insert(idx, field)
        return new_record

    @classmethod
    def create_or_update(cls, data, id_=None, dbcommit=False, reindex=False,
                         vendor=None, **kwargs):
        """Create or update ebook record."""
        pid = build_ebook_pid(data, vendor)
        record = cls.get_record_by_pid(pid)
        if record is not None:
            merged_data = cls._merge_uri(data, record)
            record.update(merged_data, dbcommit=dbcommit, reindex=reindex,
                          forceindex=reindex)
            return record, 'UPDATE'
        else:
            created_record = cls.create(
                data,
                id_=None,
                vendor=vendor,
                dbcommit=dbcommit,
                reindex=reindex,
                forceindex=reindex
            )
            return created_record, 'CREATE'

    @classmethod
    def _delete_uri(cls, not_available_record, old_record, url):
        """Merge new and old records."""
        field = cls.uri_key
        not_available_e_res = not_available_record.get(field)
        # change all tuples to lists
        # the dojson produces tuples and we have lists in the record
        for e_res in not_available_e_res:
            for key, value in e_res.items():
                if isinstance(value, tuple):
                    e_res[key] = list(value)

        old_e_res = old_record.get(field)
        epub_count = 0
        for e_res in not_available_e_res:
            # check if exists!
            res_url = e_res.get('uniform_resource_identifier')
            if res_url.startswith(url):
                if e_res in old_e_res:
                    epub_count += 1
                    old_e_res.remove(e_res)
                    old_record['__order__'].remove(field)

        return old_record, epub_count

    @classmethod
    def remove_uri(cls, data, vendor=None, url=None,
                   dbcommit=False, reindex=False):
        """Create or update ebook record."""
        pid = build_ebook_pid(data, vendor)
        record = cls.get_record_by_pid(pid)
        if record is not None:
            merged_data, epub_count = cls._delete_uri(data, record, url)
            record.replace(merged_data, dbcommit=dbcommit, reindex=reindex,
                           forceindex=reindex)
            return record, 'REMOVE URIs: {count}'.format(count=epub_count)
        data['pid'] = pid
        return data, 'REMOVE missing'

    @classmethod
    def create(
        cls,
        data,
        id_=None,
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

    def delete(self, force=False, dbcommit=False, delindex=False):
        """Delete record and persistent identifier."""
        persistent_identifier = self.get_persistent_identifier(self.id)
        persistent_identifier.delete()
        self = super(Ebook, self).delete(force=force)
        if dbcommit:
            self.dbcommit()
        if delindex:
            self.delete_from_index()
        return self

    @classmethod
    def get_record_by_id(cls, id, with_deleted=False):
        """Get ils record by uuid."""
        return super(Ebook, cls).get_record(id, with_deleted=with_deleted)

    @classmethod
    def get_record_by_pid(cls, pid, with_deleted=False):
        """Get ebook record by pid value."""
        assert cls.provider
        try:
            persistent_identifier = PersistentIdentifier.get(
                cls.provider.pid_type,
                pid
            )
            return super(Ebook, cls).get_record(
                persistent_identifier.object_uuid,
                with_deleted=with_deleted
            )
        except NoResultFound:
            return None
        except PIDDoesNotExistError:
            return None

    def update(self, data, dbcommit=False, reindex=False, forceindex=False):
        """Update data for record."""
        super(Ebook, self).update(data)
        super(Ebook, self).commit()
        if dbcommit:
            self.dbcommit(reindex)
        if reindex:
            self.reindex(forceindex=forceindex)
        return self

    def replace(self, data, dbcommit=False, reindex=False, forceindex=False):
        """Replace data in record."""
        new_data = copy.deepcopy(data)
        pid = new_data.get('pid')
        if not pid:
            raise EbookError.PidMissing(
                'missing pid={pid}'.format(pid=self.pid)
            )
        self.clear()
        self = self.update(new_data, dbcommit=dbcommit, reindex=reindex,
                           forceindex=forceindex)
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

    def delete_from_index(self):
        """Delete record from index."""
        try:
            RecordIndexer().delete(self)
        except NotFoundError:
            pass

    @classmethod
    def get_persistent_identifier(cls, pid):
        """Get Persistent Identifier."""
        return PersistentIdentifier.get_by_object(
            cls.provider.pid_type,
            cls.object_type,
            pid
        )

    @classmethod
    def _get_all(cls, with_deleted=False):
        """Get all persistent identifier records."""
        query = PersistentIdentifier.query.filter_by(
            pid_type=cls.provider.pid_type
        )
        if not with_deleted:
            query = query.filter_by(status=PIDStatus.REGISTERED)
        return query

    @classmethod
    def get_all_pids(cls, with_deleted=False):
        """Get all records pids. Return a generator iterator."""
        query = cls._get_all(with_deleted=with_deleted)
        for identifier in query:
            yield identifier.pid_value

    @classmethod
    def get_all_ids(cls, with_deleted=False):
        """Get all records uuids. Return a generator iterator."""
        query = cls._get_all(with_deleted=with_deleted)
        for identifier in query:
            yield identifier.object_uuid

    @classmethod
    def count(cls, with_deleted=False):
        """Get record count."""
        return cls._get_all(with_deleted=with_deleted).count()

    @property
    def pid(self):
        """Get ebook record pid value."""
        return self.get('pid')

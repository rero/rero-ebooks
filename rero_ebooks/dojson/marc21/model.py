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

"""Marc21 data conversion."""

from dojson import Overdo

marc21 = Overdo(entry_point_group="rero_ebooks.marc21")
"""MARC 21 Format for Bibliographic Data."""


@marc21.over("__order__", "__order__")
def order(self, key, value):
    """Preserve order of datafields."""
    data_order = []
    for field in value:
        name = marc21.index.query(field)
        name = name[0] if name else field
        data_order.append(name)

    return data_order

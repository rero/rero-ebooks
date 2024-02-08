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

"""Test ApiCantook."""

from __future__ import absolute_import, print_function

from rero_ebooks.cantook.api import ApiCantook


def test_add_nonpublic_note(app, config_vs):
    """Test cantook merge."""

    apicantook = ApiCantook(config=config_vs)
    record = {
        "electronic_location_and_access": [
            {
                "electronic_format_type": "epub",
                "uniform_resource_identifier": "http://mediatheque-valais.cantookstation.eu/"
                "resources/583fc6ef2357943cb70c641d",
                "materials_specified": "Texte int\u00e9gral",
                "access_method": "HTTP",
                "relationship": "Resource",
            }
        ]
    }
    record = apicantook.add_nonpublic_note(record)
    assert record["electronic_location_and_access"][0]["nonpublic_note"] == "mv-cantook"

    record = {
        "electronic_location_and_access": [
            {
                "uniform_resource_identifier": "https://www.edenlivres.fr/p/227276",
                "materials_specified": "Extrait",
                "access_method": "HTTP",
                "relationship": "Related resource",
            }
        ]
    }
    record = apicantook.add_nonpublic_note(record)
    assert record["electronic_location_and_access"][0].get("nonpublic_note") is None

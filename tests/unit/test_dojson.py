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

"""Test JSON to JSON transformation."""

import json
from collections import OrderedDict

from rero_ebooks.dojson.json.model import cantook_json


def test_json_system_control_number():
    """Test System control number transformation."""
    data = {"id": "1234"}
    assert cantook_json.do(data) == {
        "__order__": [
            "leader",
            "fixed_length_data_elements",
            "other_standard_identifier",
            "system_control_number",
        ],
        "fixed_length_data_elements": "000000n########xx#|||||||||||||||||###|u",
        "other_standard_identifier": [
            {
                "standard_number_or_code": "cantook/1234",
                "type_of_standard_number_or_code": "Unspecified type of standard number or code",
            }
        ],
        "system_control_number": {"system_control_number": "cantook-1234"},
        "leader": {
            "base_address_of_data": 0,
            "bibliographic_level": "monograph_item",
            "character_coding_scheme": "ucs_unicode",
            "descriptive_cataloging_form": "unknown",
            "encoding_level": "not_applicable",
            "indicator_count": 2,
            "length_of_the_implementation_defined_portion": 0,
            "length_of_the_length_of_field_portion": 4,
            "length_of_the_starting_character_position_portion": 5,
            "record_length": 0,
            "record_status": "corrected_or_revised",
            "subfield_code_count": 2,
            "type_of_record": "language_material",
            "undefined": 0,
        },
    }


def test_json_languages():
    """Test languages tranformation."""
    data = {"languages": ["fre"]}
    assert cantook_json.do(data) == {
        "__order__": ["language_code"],
        "language_code": [
            {"language_code_of_text_sound_track_or_separate_title": "fre"}
        ],
    }


def test_json_languages_and_translated_from():
    """Test languages and translated_from tranformation."""
    data = {"languages": ["fre"], "translated_from": ["ger"]}
    assert cantook_json.do(data) == {
        "__order__": ["language_code", "language_code"],
        "language_code": [
            {"language_code_of_text_sound_track_or_separate_title": "fre"},
            {
                "language_code_of_original": "ger",
                "translation_indication": "Item is or includes a translation",
            },
        ],
    }


def test_json_title():
    """Test title tranformation."""
    data = {"title": "titre"}
    assert cantook_json.do(data) == {
        "__order__": ["title_statement"],
        "title_statement": {"title": "titre"},
    }


def test_json_title_and_subtitle():
    """Test title and subtitle tranformation."""
    data = {"title": "titre", "subtitle": "sous-titre"}
    assert cantook_json.do(data) == {
        "__order__": ["title_statement"],
        "title_statement": {"title": "titre", "remainder_of_title": "sous-titre"},
    }


def test_json_publisher_name():
    """Test publisher name tranformation."""
    data = {"publisher_name": "Editions Gallimard"}
    assert cantook_json.do(data) == {
        "__order__": [
            "production_publication_distribution_manufacture" "_and_copyright_notice"
        ],
        "production_publication_distribution_manufacture_and_copyright_notice": {
            "name_of_producer_publisher_distributor_manufacturer": "Editions Gallimard",
            "function_of_entity": "Publication",
        },
    }


def test_json_physical_description():
    """Test physical description tranformation."""
    data = {"page_count": "1234"}
    assert cantook_json.do(data) == {
        "__order__": ["physical_description"],
        "physical_description": [{"extent": "1234 pages"}],
    }


def test_json_summary():
    """Test summary tranformation."""
    data = {"summary": "résumé"}
    assert cantook_json.do(data) == {
        "__order__": ["summary"],
        "summary": {"summary": "résumé"},
    }


def test_index_term_uncontrolled():
    """Test Index term uncontrolled transformation."""
    data = {
        "classifications": [
            {
                "standard": "bisac",
                "identifiers": ["TRV015000"],
                "captions": [{"fr": None, "en": None}],
            },
            {
                "standard": "cantook",
                "identifiers": ["tourism-travel"],
                "captions": [{"fr": "Tourisme et voyages", "en": "Tourism & Travel"}],
            },
            {
                "standard": "feedbooks",
                "identifiers": ["FBTRV015000"],
                "captions": [{"fr": "Moyen-Orient", "en": "Middle East"}],
            },
        ]
    }
    assert cantook_json.do(data) == {
        "__order__": ["index_term_uncontrolled", "index_term_uncontrolled"],
        "index_term_uncontrolled": [
            {
                "__order__": ["uncontrolled_term", "uncontrolled_term"],
                "uncontrolled_term": ["Tourisme et voyages", "Tourism & Travel"],
            },
            {
                "__order__": ["uncontrolled_term", "uncontrolled_term"],
                "uncontrolled_term": ["Moyen-Orient", "Middle East"],
            },
        ],
    }


def test_json_added_entry_personal_name():
    """Test Added entry personal name transformation."""
    data = {
        "contributors": [
            {"first_name": "Victor", "last_name": "Hugo", "nature": "author"},
            {"last_name": "Toto", "nature": "translated_by"},
        ]
    }
    assert cantook_json.do(data) == {
        "__order__": ["added_entry_personal_name", "added_entry_personal_name"],
        "added_entry_personal_name": [
            {
                "type_of_personal_name_entry_element": "Surname",
                "personal_name": "Hugo, Victor",
                "relator_code": "aut",
            },
            {
                "type_of_personal_name_entry_element": "Forename",
                "personal_name": "Toto",
                "relator_code": "trl",
            },
        ],
    }


def test_json_media():
    """Test media tranformation."""
    data = {
        "media": [
            {
                "nature": "epub",
                "key_type": "isbn13",
                "id": "immateriel.frO588299-9791028508067-epub",
                "key": "9791028508067",
                "issued_on": "2019-04-09T06:00:00+02:00",
                "current_holds": 0,
            },
            {
                "nature": "paper",
                "key_type": "isbn13",
                "id": "immateriel.frO588299-9791028503154-paper",
                "key": "9791028514563",
                "issued_on": None,
                "current_holds": 0,
            },
        ]
    }
    assert cantook_json.do(data) == {
        "__order__": [
            "international_standard_book_number",
            "production_publication_distribution_manufacture" "_and_copyright_notice",
            "electronic_location_and_access",
        ],
        "international_standard_book_number": {
            "international_standard_book_number": "9791028508067"
        },
        "production_publication_distribution_manufacture_and_copyright_notice": {
            "date_of_production_publication_distribution_manufacture"
            "_or_copyright_notice": "2019"
        },
        "electronic_location_and_access": [{"electronic_format_type": "epub"}],
    }


def test_json_cover_flipbook_link():
    """Test cover, flipbook, link tranformation."""
    data = {
        "cover": "http://images.immateriel.fr/covers/FWK3BH5.png",
        "flipbook": "http://livre.immateriel.fr/FWK3BH5?no_sign_in=true",
        "link": "http://mediatheque-valais.cantookstation.eu/"
        "resources/58e878ce235794558ef07803",
    }

    assert cantook_json.do(data) == {
        "__order__": [
            "electronic_location_and_access",
            "electronic_location_and_access",
            "electronic_location_and_access",
        ],
        "electronic_location_and_access": [
            {
                "uniform_resource_identifier": "http://images.immateriel.fr/covers/FWK3BH5.png",
                "materials_specified": "Image de couverture",
                "access_method": "HTTP",
                "relationship": "Related resource",
            },
            {
                "uniform_resource_identifier": "http://livre.immateriel.fr/FWK3BH5?no_sign_in=true",
                "materials_specified": "Extrait",
                "access_method": "HTTP",
                "relationship": "Related resource",
            },
            {
                "uniform_resource_identifier": "http://mediatheque-valais.cantookstation.eu/"
                "resources/58e878ce235794558ef07803",
                "materials_specified": "Texte intégral",
                "access_method": "HTTP",
                "relationship": "Resource",
            },
        ],
    }


def test_json_cover_flipbook_link_media():
    """Test cover, flipbook, link, media tranformation."""

    json_data = """
    {
        "cover": "http://images.immateriel.fr/covers/FWK3BH5.png",
        "flipbook": "http://livre.immateriel.fr/FWK3BH5?no_sign_in=true",
        "link": "http://mediatheque-valais.cantookstation.eu/resources/58e878",
        "media": [
            {
                "nature": "epub",
                "key_type": "isbn13",
                "id": "immateriel.frO588299-9791028508067-epub",
                "key": "9791028508067",
                "issued_on": "2019-04-09T06:00:00+02:00",
                "current_holds": 0
            },
            {
                "nature": "paper",
                "key_type": "isbn13",
                "id": "immateriel.frO588299-9791028503154-paper",
                "key": "9791028514563",
                "issued_on": "",
                "current_holds": 0
            }
        ]
    }
    """
    data = json.loads(json_data, object_pairs_hook=OrderedDict)

    res = cantook_json.do(data)
    ref = {
        "__order__": [
            "international_standard_book_number",
            "production_publication_distribution_manufacture" "_and_copyright_notice",
            "electronic_location_and_access",
            "electronic_location_and_access",
            "electronic_location_and_access",
        ],
        "electronic_location_and_access": [
            {
                "uniform_resource_identifier": "http://images.immateriel.fr/covers/FWK3BH5.png",
                "materials_specified": "Image de couverture",
                "access_method": "HTTP",
                "relationship": "Related resource",
            },
            {
                "uniform_resource_identifier": "http://livre.immateriel.fr/FWK3BH5?no_sign_in=true",
                "materials_specified": "Extrait",
                "access_method": "HTTP",
                "relationship": "Related resource",
            },
            {
                "electronic_format_type": "epub",
                "uniform_resource_identifier": "http://mediatheque-valais.cantookstation.eu/"
                "resources/58e878",
                "materials_specified": "Texte intégral",
                "access_method": "HTTP",
                "relationship": "Resource",
            },
        ],
        "international_standard_book_number": {
            "international_standard_book_number": "9791028508067"
        },
        "production_publication_distribution_manufacture_and_copyright_notice": {
            "date_of_production_publication_distribution_manufacture"
            "_or_copyright_notice": "2019"
        },
    }
    assert ref == res


def test_json_media_cover_flipbook_link():
    """Test cover, flipbook, link tranformation.

    The difference between this test and the test
    test_json_cover_flipbook_link_media is the order of the input
    data. In this test the media data arrive first and so,
    in the result, the first element in the list
    'electronic_location_and_access' is the dict containing the key
    'electronic_format_type' (instead of the last element in the
    test: test_json_cover_flipbook_link_media).

    Both cases are used to test all parts of the implementation.
    """

    json_data = """
    {
        "media": [
            {
                "nature": "epub",
                "key_type": "isbn13",
                "id": "immateriel.frO588299-9791028508067-epub",
                "key": "9791028508067",
                "issued_on": "2019-04-09T06:00:00+02:00",
                "current_holds": 0
            },
            {
                "nature": "paper",
                "key_type": "isbn13",
                "id": "immateriel.frO588299-9791028503154-paper",
                "key": "9791028514563",
                "issued_on": "",
                "current_holds": 0
            }
        ],
        "cover": "http://images.immateriel.fr/covers/FWK3BH5.png",
        "flipbook": "http://livre.immateriel.fr/FWK3BH5?no_sign_in=true",
        "link": "http://mediatheque-valais.cantookstation.eu/resources/58e878"
    }
    """
    data = json.loads(json_data, object_pairs_hook=OrderedDict)

    res = cantook_json.do(data)
    ref = {
        "__order__": [
            "international_standard_book_number",
            "production_publication_distribution_manufacture" "_and_copyright_notice",
            "electronic_location_and_access",
            "electronic_location_and_access",
            "electronic_location_and_access",
        ],
        "electronic_location_and_access": [
            {
                "electronic_format_type": "epub",
                "uniform_resource_identifier": "http://mediatheque-valais.cantookstation.eu/"
                "resources/58e878",
                "materials_specified": "Texte intégral",
                "access_method": "HTTP",
                "relationship": "Resource",
            },
            {
                "uniform_resource_identifier": "http://images.immateriel.fr/covers/FWK3BH5.png",
                "materials_specified": "Image de couverture",
                "access_method": "HTTP",
                "relationship": "Related resource",
            },
            {
                "uniform_resource_identifier": "http://livre.immateriel.fr/FWK3BH5?no_sign_in=true",
                "materials_specified": "Extrait",
                "access_method": "HTTP",
                "relationship": "Related resource",
            },
        ],
        "international_standard_book_number": {
            "international_standard_book_number": "9791028508067"
        },
        "production_publication_distribution_manufacture_and_copyright_notice": {
            "date_of_production_publication_distribution_manufacture"
            "_or_copyright_notice": "2019"
        },
    }
    assert ref == res

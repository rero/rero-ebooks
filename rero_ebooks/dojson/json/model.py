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
# waive the privileges and immunities granted to it by virtue of its
# status as an Intergovernmental Organization or submit itself
# to any jurisdiction.

"""Cantook json record transformation."""

from dojson import Overdo, utils


class Underdo(Overdo):
    """Ordered overdo.

    Order fields conforming to the Marc21 fields order.
    """

    def do(self, blob, ignore_missing=True, exception_handlers=None):
        """Translate blob values and instantiate new model instance."""
        res = super(Underdo, self).do(blob, ignore_missing, exception_handlers)

        order = [
            'leader',
            'control_number',
            'fixed_length_data_elements',
            'international_standard_book_number',
            'other_standard_identifier',
            'system_control_number',
            'language_code',
            'title_statement',
            'production_publication_distribution_manufacture'  # + next line
            '_and_copyright_notice',
            'physical_description',
            'page_count',
            'summary',
            'index_term_uncontrolled',
            'added_entry_personal_name',
            'electronic_location_and_access',
        ]

        # get all keys from reas as list
        keys = [*res]
        # sort the list with help of order list
        keys = sorted(keys, key=lambda x: order.index(x))
        # correct list for multiple entries
        all_keys = []
        for key in keys:
            if type(res[key]) == list:
                for count in range(0, len(res[key])):
                    all_keys.append(key)
            else:
                all_keys.append(key)
        res['__order__'] = all_keys

        return res


cantook_json = Underdo()
"""rero_ebook Format for Cantook Data."""


@cantook_json.over('system_control_number', 'id')
def system_control_number(self, key, value):
    """System control number transformation.

    The id field is transforme as system_control_number and
    other_standard_identifier

    The system_control_number is used in the Marc21 035 field.
    The other_standard_identifier is used in the Marc21 024 field.
    A Marc21 Leader data is added.
    """
    self['leader'] = {
        'base_address_of_data': 0,
        'bibliographic_level': 'monograph_item',
        'character_coding_scheme': 'ucs_unicode',
        'descriptive_cataloging_form': 'unknown',
        'encoding_level': 'not_applicable',
        'indicator_count': 2,
        'length_of_the_implementation_defined_portion': 0,
        'length_of_the_length_of_field_portion': 4,
        'length_of_the_starting_character_position_portion': 5,
        'record_length': 0,
        'record_status': 'corrected_or_revised',
        'subfield_code_count': 2,
        'type_of_record': 'language_material',
        'undefined': 0
    }
    self['other_standard_identifier'] = [{
        'standard_number_or_code': 'cantook/' + value,
        'type_of_standard_number_or_code':
            'Unspecified type of standard number or code'
    }]
    return {'system_control_number': 'cantook-' + value}


@cantook_json.over('language_code', 'languages|translated_from')
def language_code(self, key, value):
    """Language codes transformation.

    The language codes are used in the Marc21 041 field.
    """
    result = self.get('language_code', [])
    if value:
        for lang in utils.force_list(value):
            if key == 'languages':
                result.append(
                    {'language_code_of_text_sound_track_or_separate_title':
                        lang}
                )
            else:
                result.append({
                    'language_code_of_original': lang,
                    'translation_indication':
                        'Item is or includes a translation'
                })
    return result


@cantook_json.over('title_statement', 'title|subtitle')
def title_statement(self, key, value):
    """Title statement transformation.

    The title and subtitle are used in the Marc21 245 field.
    """
    return_value = self.get('title_statement', {})
    if value:
        if key == 'title':
            return_value['title'] = value
        elif key == 'subtitle':
            return_value['remainder_of_title'] = value
    return return_value


@cantook_json.over(None, 'publisher_name')
@utils.filter_values
@utils.ignore_value
def publisher_name(self, key, value):
    """Publisher name transformation.

    The publisher_name is used in the Marc21 264 field.
    """
    self.setdefault(
        'production_publication_distribution_manufacture_and_copyright_notice',
        {}
    )
    self[
        'production_publication_distribution_manufacture_and_copyright_notice'
    ].update({
        'name_of_producer_publisher_distributor_manufacturer': value,
        'function_of_entity': 'Publication'
    })
    return None


@cantook_json.over('physical_description', 'page_count')
@utils.for_each_value
@utils.filter_values
def physical_description(self, key, value):
    """Physical description transformation.

    extent (Number of physical pages, volumes...): Marc21 300 $a field.
    """
    return {'extent': str(value)}


@cantook_json.over('summary', 'summary')
def summary(self, key, value):
    """Summary transformation."""
    return {'summary': value}


@cantook_json.over('index_term_uncontrolled', 'classifications')
def index_term_uncontrolled(self, key, value):
    """Index term uncontrolled transformation.

    index_term_uncontrolled: Marc21 653 field.
    """
    index_term_uncontrolled = []
    for classification in value:
        for caption in classification.get('captions', []):
            uncontrolled_term = []
            order = []
            fr = caption.get('fr')
            need_to_append_term = False
            if fr:
                uncontrolled_term.append(fr)
                order.append('uncontrolled_term')
                need_to_append_term = True
            en = caption.get('en')
            if en:
                uncontrolled_term.append(en)
                order.append('uncontrolled_term')
                need_to_append_term = True
            if need_to_append_term:
                index_term_uncontrolled.append({
                    '__order__': order,
                    'uncontrolled_term': uncontrolled_term
                })
    return index_term_uncontrolled


@cantook_json.over('added_entry_personal_name', 'contributors')
@utils.for_each_value
@utils.filter_values
def added_entry_personal_name(self, key, value):
    """Added entry personal name transformation.

    added_entry_personal_name: Marc21 700 field.
    """
    result = {}
    names = []
    result['type_of_personal_name_entry_element'] = 'Forename'
    if value.get('first_name'):
        names.append(value.get('first_name'))
    if value.get('last_name'):
        names.insert(0, value.get('last_name'))
    result['personal_name'] = ', '.join(names)
    if len(names) > 1:
        result['type_of_personal_name_entry_element'] = 'Surname'
    if value.get('nature') == 'author':
        result['relator_code'] = 'aut'
    elif value.get('nature') == 'translated_by':
        result['relator_code'] = 'trl'
    return result


@cantook_json.over('electronic_location_and_access', 'cover|flipbook|link')
def electronic_location_and_access_from_cover_flipbook_link(self, key, value):
    """Transformation of cover, flipbook and link data.

    electronic_location_and_access: Marc21 856 field.
    """
    result = self.get('electronic_location_and_access', [])
    if value and key == 'cover':
        result.append(
            {
                'uniform_resource_identifier': value,
                'materials_specified': 'Image de couverture',
                'access_method': 'HTTP',
                'relationship': 'Related resource'
            }
        )
    elif value and key == 'flipbook':
        result.append(
            {
                'uniform_resource_identifier': value,
                'materials_specified': 'Extrait',
                'access_method': 'HTTP',
                'relationship': 'Related resource'
            }
        )
    elif key == 'link':
        need_to_append_link_data = True
        for data in result:
            if data.get('electronic_format_type'):
                data['uniform_resource_identifier'] = value
                data['materials_specified'] = 'Texte intégral'
                data['access_method'] = 'HTTP'
                data['relationship'] = 'Resource'
                need_to_append_link_data = False
        if need_to_append_link_data:
            result.append(
                {
                    # 'electronic_format_type' : is added from media:nature
                    'uniform_resource_identifier': value,
                    'materials_specified': 'Texte intégral',
                    'access_method': 'HTTP',
                    'relationship': 'Resource'
                }
            )
    return result


@cantook_json.over(None, 'media')
@utils.for_each_value
@utils.filter_values
@utils.ignore_value
def transformation_from_media(self, key, value):
    """Media data transformation.

    international_standard_book_number is added: Marc21 020 field.
    electronic_format_type is added to the field
    electronic_location_and_access having 'Ressource' relationship.
    production_publication_distribution_manufacture_and_copyright_notice
    :date_of_production_publication_distribution_manufacture is added
    (Marc21 264 $c field).
    """
    if value.get('key'):
        self['international_standard_book_number'] = {
            'international_standard_book_number': value.get('key')
        }
    if value.get('nature'):
        self.setdefault('electronic_location_and_access', [])
        location_and_access = self['electronic_location_and_access']
        need_to_append_link_data = True
        for data in location_and_access:
            if data.get('relationship') == 'Resource':
                data['electronic_format_type'] = value.get('nature')
                need_to_append_link_data = False
        if need_to_append_link_data:
            location_and_access.append({
                'electronic_format_type': value.get('nature')})
    if value.get('issued_on'):
        self.setdefault(
            'production_publication_distribution_manufacture'
            '_and_copyright_notice',
            {}
        )
        self['production_publication_distribution_manufacture'
             '_and_copyright_notice'].update(
            {
                'date_of_production_publication_distribution_manufacture'
                '_or_copyright_notice': value.get('issued_on')[:4]
            })
    return None

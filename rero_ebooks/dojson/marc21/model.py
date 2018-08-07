# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 data conversion."""

from dojson import Overdo, utils

marc21 = Overdo(entry_point_group='rero_ebooks.marc21')
"""MARC 21 Format for Bibliographic Data."""


@marc21.over('__order__', '__order__')
def order(self, key, value):
    """Preserve order of datafields."""
    order = []
    for field in value:
        name = marc21.index.query(field)
        if name:
            name = name[0]
        else:
            name = field
        order.append(name)

    return order

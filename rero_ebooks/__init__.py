# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 RERO.
#
# RERO Ebooks is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""RERO Ebooks."""

from __future__ import absolute_import, print_function

from .ext import ReroEBooks
from .version import __version__

__all__ = ('__version__', 'ReroEBooks')

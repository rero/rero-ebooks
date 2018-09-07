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

FROM python:3.5-slim

LABEL maintainer="software@rero.ch"
LABEL description="Ebooks repository for RERO."

RUN apt-get update && apt-get install -y curl git gcc gnupg \
    && apt-get install -y nodejs \
    && pip install -U setuptools pip && \
    pip install -U virtualenv


# Add Invenio sources to `code` and work there:
WORKDIR /ebooks/ebooks/src/rero-ebooks
COPY setup.py /ebooks/ebooks/src/rero-ebooks/
COPY setup.cfg /ebooks/ebooks/src/rero-ebooks/
COPY babel.ini /ebooks/ebooks/src/rero-ebooks/
COPY MANIFEST.in /ebooks/ebooks/src/rero-ebooks/
COPY README.rst /ebooks/ebooks/src/rero-ebooks/
COPY requirements.txt /ebooks/ebooks/src/rero-ebooks/
COPY rero_ebooks /ebooks/ebooks/src/rero-ebooks/rero_ebooks
COPY scripts/setup /ebooks/scripts/setup
COPY data/oaisources.yml /ebooks/data/oaisources.yml

# # Run container as user `invenio` with UID `1000`, which should match
# # current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' invenio && \
     chown -R invenio:invenio /ebooks

USER invenio

SHELL ["/bin/bash", "-c"]
WORKDIR /ebooks
RUN virtualenv ebooks

RUN source ebooks/bin/activate && \
    pip install -r /ebooks/ebooks/src/rero-ebooks/requirements.txt && \
    pip install ebooks/src/rero-ebooks && \
    pip install flower && \
    pip install gunicorn

USER root
RUN rm -rf /var/lib/apt/lists/*

USER invenio
CMD ["/ebooks/ebooks/bin/gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "invenio_app.wsgi"]

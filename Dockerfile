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

ARG VERSION=latest
FROM rero/rero-ebooks-base:${VERSION}

USER 0

ENV WORKING_DIR=/invenio
WORKDIR ${WORKING_DIR}/src
ENV INVENIO_INSTANCE_PATH=${WORKING_DIR}/var/instance

RUN chown -R invenio:invenio ${WORKING_DIR}

USER 1000

ENV INVENIO_COLLECT_STORAGE='flask_collect.storage.file'
RUN poetry run bootstrap --deploy

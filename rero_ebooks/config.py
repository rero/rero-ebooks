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

"""Default configuration for RERO Ebooks.

You overwrite and set instance-specific configuration by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``
"""

from __future__ import absolute_import, print_function

from datetime import timedelta


def _(x):
    """Identity function used to trigger string extraction."""
    return x


# Rate limiting
# =============
RATELIMIT_STORAGE_URL = 'redis://localhost:6379/3'
RATELIMIT_DEFAULT = '5000/second'
RATELIMIT_ENABLED = False


# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'en'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
#: Other supported languages (do not include the default language in list).
I18N_LANGUAGES = [
    # ('fr', _('French'))
]

# Base templates
# ==============
#: Global base template.
BASE_TEMPLATE = 'invenio_theme/page.html'
#: Cover page base template (used for e.g. login/sign-up).
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
#: Footer base template.
FOOTER_TEMPLATE = 'rero_ebooks/footer.html'
#: Header base template.
HEADER_TEMPLATE = 'rero_ebooks/header.html'
#: Settings base template.
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

# Theme configuration
# ===================
#: Site name
THEME_SITENAME = _('RERO Ebooks')
#: Use default frontpage.
THEME_FRONTPAGE = False
#: Frontpage title.
THEME_FRONTPAGE_TITLE = _('RERO Ebooks')
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'rero_ebooks/frontpage.html'
#: Footer base template.
THEME_FOOTER_TEMPLATE = FOOTER_TEMPLATE
#: Header base template.
THEME_HEADER_TEMPLATE = HEADER_TEMPLATE


# Email configuration
# ===================
#: Email address for support.
SUPPORT_EMAIL = "software@rero.ch"
#: Disable email sending by default.
MAIL_SUPPRESS_SEND = True

# Assets
# ======
#: Static files collection method (defaults to copying files).
COLLECT_STORAGE = 'flask_collect.storage.file'

# Accounts
# ========
#: Email address used as sender of account registration emails.
SECURITY_EMAIL_SENDER = SUPPORT_EMAIL
#: Email subject for account registration emails.
SECURITY_EMAIL_SUBJECT_REGISTER = _(
    "Welcome to RERO Ebooks!")
#: Redis session storage URL.
ACCOUNTS_SESSION_REDIS_URL = 'redis://localhost:6379/1'

# Celery configuration
# ====================

BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#: URL of message broker for Celery (default is RabbitMQ).
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#: URL of backend for result storage (default is Redis).
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
#: Scheduled tasks configuration (aka cronjobs).
# imports have to be configured in setup.py:invenio_celery.tasks
CELERY_BEAT_SCHEDULE = {
    'indexer': {
        'task': 'invenio_indexer.tasks.process_bulk_queue',
        'schedule': timedelta(minutes=5),
    },
    # 'Harvester-VS': {
    #     'task': 'invenio_oaiharvester.tasks.list_records_from_dates',
    #     'schedule': timedelta(minutes=60),
    #     'kwargs': dict(name='VS')
    # },
    # 'Harvester-NJ': {
    #     'task': 'invenio_oaiharvester.tasks.list_records_from_dates',
    #     'schedule': timedelta(minutes=60),
    #     'kwargs': dict(name='NJ')
    # },
    # 'Apiharvester-NJ': {
    #     'task': 'rero_ebooks.apiharvester.tasks.harvest_records',
    #     'schedule': timedelta(minutes=60),
    #     'kwargs': dict(name='NJ'),
    # },
    # 'Apiharvester-VS': {
    #     'task': 'rero_ebooks.apiharvester.tasks.harvest_records',
    #     'schedule': timedelta(minutes=60),
    #     'kwargs': dict(name='VS')
    # },
}
CELERY_BROKER_HEARTBEAT = 0

# Database
# ========
#: Database URI including user and password
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://rero-ebooks:rero-ebooks@localhost/rero-ebooks'
# disable record versioning
DB_VERSIONING = False

# JSONSchemas
# ===========
#: Hostname used in URLs for local JSONSchemas.
JSONSCHEMAS_HOST = 'ebooks.rero.ch'

# Flask configuration
# ===================
# See details on
# http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values

#: Secret key - each installation (dev, production, ...) needs a separate key.
#: It should be changed before deploying.
SECRET_KEY = 'CHANGE_ME'
#: Max upload size for form data via application/mulitpart-formdata.
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
#: Sets cookie with the secure flag by default
SESSION_COOKIE_SECURE = True
#: Since HAProxy and Nginx route all requests no matter the host header
#: provided, the allowed hosts variable is set to localhost. In production it
#: should be set to the correct host and it is strongly recommended to only
#: route correct hosts to the application.
APP_ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# TODO: review theses rules for security purposes
APP_DEFAULT_SECURE_HEADERS = {
    # disabled as https is not used by the application:
    # https is done by the haproxy
    'force_https': False,
    'force_https_permanent': False,
    'force_file_save': False,
    'frame_options': 'sameorigin',
    'frame_options_allow_from': None,
    'strict_transport_security': True,
    'strict_transport_security_preload': False,
    'strict_transport_security_max_age': 31556926,  # One year in seconds
    'strict_transport_security_include_subdomains': True,
    'content_security_policy': {
        'default-src': ['*'],
        'img-src': [
            '*',
            "'self'",
            'data:'
        ],
        'style-src': [
            '*',
            "'unsafe-inline'"
        ],
        'script-src': [
            "'self'",
            "'unsafe-eval'",
            "'unsafe-inline'",
            # '*.rero.ch',
            'https://www.googletagmanager.com',
            'https://www.google-analytics.com'
        ]
    },
    'content_security_policy_report_uri': None,
    'content_security_policy_report_only': False,
    'session_cookie_secure': True,
    'session_cookie_http_only': True,
}

# Indexer
# =======
#: default ES index
INDEXER_DEFAULT_INDEX = "ebooks-ebook-v1.0.0"
#: default ES document type
INDEXER_DEFAULT_DOC_TYPE = "ebook-v1.0.0"

# OAI-PMH
# =======
#: OAI prefix
OAISERVER_ID_PREFIX = 'oai:ebooks.rero.ch:'
#: OAI fetcher
OAISERVER_CONTROL_NUMBER_FETCHER = 'ebook'
#: OAI default ES index
OAISERVER_RECORD_INDEX = 'ebooks'

OAISERVER_XSL_URL = '/static/xsl/oai.xsl'

OAISERVER_ADMIN_EMAILS = [
    'software@rero.ch',
]

# Debug
# =====
# Flask-DebugToolbar is by default enabled when the application is running in
# debug mode. More configuration options are available at
# https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration

#: Switches off incept of redirects by Flask-DebugToolbar.
DEBUG_TB_INTERCEPT_REDIRECTS = False

RECORDS_REST_ENDPOINTS = dict(
    ebook=dict(
        pid_type='ebook',
        pid_minter='ebook',
        pid_fetcher='ebook',
        search_class="rero_ebooks.api:EbooksSearch",
        indexer_class="invenio_indexer.api:RecordIndexer",
        record_class="rero_ebooks.api:Ebook",
        search_index=None,
        search_type=None,
        record_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_search'),
        },
        list_route='/ebooks/',
        item_route=('/ebooks/'
                    '<pid((ebook, record_class="rero_ebooks.api:Ebook"))'
                    ':pid_value>'),
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
    ),
)

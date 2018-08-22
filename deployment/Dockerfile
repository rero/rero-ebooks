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

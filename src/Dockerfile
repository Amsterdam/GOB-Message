# syntax=docker/dockerfile:1
FROM amsterdam/gob_wheelhouse:3.9-buster as wheelhouse
MAINTAINER datapunt@amsterdam.nl


# Application stage.
FROM amsterdam/gob_baseimage:3.9-buster as application
MAINTAINER datapunt@amsterdam.nl
# GOB base image: SQL Server driver.

# libxml
RUN apt-get install -y libxml2-dev libxmlsec1-dev

# Fill the wheelhouse.
COPY --from=wheelhouse /opt/wheelhouse /opt/wheelhouse

# Install gobmessage in /app folder.
WORKDIR /app

# Install required Python packages.
COPY requirements.txt /app/
RUN LIBGDAL_VERSION=$(gdal-config --version) pip install --no-cache-dir \
	--find-links /opt/wheelhouse --requirement requirements.txt
RUN rm requirements.txt
# Wheelhouse cleanup.
RUN rm -rf /opt/wheelhouse

# Copy gobmessage module.
COPY gobmessage gobmessage

# Create directory for client certs
RUN mkdir -p /certs/gob/ && chmod -R 755 /certs

# Copy alembic config
COPY alembic alembic
COPY alembic.ini alembic.ini

# OAuth2 Proxy
COPY ./oauth2-proxy oauth2-proxy
COPY ./oauth2-proxy.cfg oauth2-proxy.cfg
RUN chmod 755 oauth2-proxy
RUN mkdir -p /var/log/oauth2-proxy && chown datapunt /var/log/oauth2-proxy

USER datapunt

CMD uwsgi

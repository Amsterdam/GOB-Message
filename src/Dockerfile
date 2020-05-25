FROM amsterdam/python:3.7-buster
MAINTAINER datapunt@amsterdam.nl

# Install gobmessage in /app folder
WORKDIR /app

# Install required Python packages
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Copy gobmessage module
COPY gobmessage gobmessage

CMD uwsgi

#!/bin/bash

# Alertsd Ubuntu Installer
# This has been tested on a vanilla Trusty install in AWS. 
# The steps are basically the same for Centos 7, but the package names are different, the users are different, and the "adduser" call to modify the group will be different.

# Packages and what they're for:
# 
# rabbitmq-server -- this is the message queue that celery will use for scheduling tasks. Redis is an alternative here.
# celeryd -- this is the task queue; it uses rabbitmq as a backend
# python-django -- this is the framework this whole thing is written in
# gunicorn -- this is the WSGI server that is used for tying django to nginx
# supervisor -- this handles init duties for gunicorn/wsgi
# nginx -- The amazing HTTP server that handles port 80 for us
# python-pip -- pip is a package installer for python. It is used to grab additional dependencies below

apt-get update
apt-get install -y rabbitmq-server celeryd python-django gunicorn supervisor nginx python-pip

# see here: http://stackoverflow.com/questions/27003492/celeryd-with-rabbitmq-hangs-on-mingle-searching-for-neighbors-but-plain-cele/27011229#27011229
sudo apt-get remove -y librabbitmq1

# Python dependencies:
#
# DjangoRestless/restless -- restless is the rest framework we use in django for the REST api

pip install DjangoRestless restless

# create the database models
python manage.py syncdb --noinput
# create the plugin entries
python manage.py syncplugins

# set up the db so it can be accessed by both celery workers and the django api
chmod 660 db.sqlite3
adduser celery www-data

# copy the sources to /opt
rsync -av --exclude=.git --exclude="*.pyc" ./ /opt/alertsd/
[[ -d /opt/alertsd/run ]] || mkdir /opt/alertsd/run
chown -R www-data. /opt/alertsd/

# copy the system configs to their proper locations 
# NOTE: this will overwrite existing configs, so doing this if you're using these things for other stuff could be detrimental!
cp conf/nginx/alertsd.conf /etc/nginx/conf.d/
cp conf/supervisor/alertsd.conf /etc/supervisor/conf.d/
cp conf/celeryd/celeryd /etc/default/

# restart the services to pick up the new configs:

# django
service supervisor restart
# celery worker
service celeryd restart
# nginx
service nginx restart

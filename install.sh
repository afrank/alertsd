#!/bin/bash

apt-get update
apt-get install -y rabbitmq-server celeryd python-django gunicorn supervisor nginx python-pip

# see here: http://stackoverflow.com/questions/27003492/celeryd-with-rabbitmq-hangs-on-mingle-searching-for-neighbors-but-plain-cele/27011229#27011229
sudo apt-get remove -y librabbitmq1

pip install DjangoRestless restless

python manage.py syncdb --noinput

rsync -av --exclude=.git --exclude="*.pyc" ./ /opt/alertsd/
[[ -d /opt/alertsd/run ]] || mkdir /opt/alertsd/run
chown -R www-data. /opt/alertsd/

cp conf/nginx/alertsd.conf /etc/nginx/conf.d/
cp conf/supervisor/alertsd.conf /etc/supervisor/conf.d/
cp conf/celeryd/celeryd /etc/default/

service supervisor restart
service celeryd restart
service nginx restart

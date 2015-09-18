#!/bin/bash

apt-get install rabbitmq-server celeryd python-django gunicorn supervisor nginx python-pip
pip install DjangoRestless

python manage.php syncdb

rsync -av --exclude=.git --exclude="*.pyc" ./ /opt/alertsd/
[[ -d /opt/alertsd/run ]] || mkdir /opt/alertsd/run
chown -R www-data. /opt/alertsd/

cp conf/nginx/alertsd.conf /etc/nginx/conf.d/
cp conf/supervisor/alertsd.conf /etc/supervisor/conf.d/
cp conf/celeryd/celeryd /etc/default/

service supervisor restart
service celeryd restart
service nginx restart

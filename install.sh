#!/bin/bash

rsync -av --exclude=.git --exclude="*.pyc" ./ /opt/alertsd/
[[ -d /opt/alertsd/run ]] || mkdir /opt/alertsd/run
chown -R www-data. /opt/alertsd/
cp conf/nginx/alertsd.conf /etc/nginx/conf.d/
cp conf/supervisor/alertsd.conf /etc/supervisor/conf.d/
cp conf/celeryd/celeryd /etc/default/

# TODO do pip/apt-get stuff here

service supervisor restart
service celeryd restart
service nginx restart

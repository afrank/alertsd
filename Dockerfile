FROM ubuntu:trusty
MAINTAINER Adam Frank <adam@antilogo.org>

RUN apt-get update && \
    apt-get install -y rabbitmq-server celeryd python-django gunicorn supervisor nginx python-pip && \
    apt-get remove -y librabbitmq1

# re: librabbitmq1 -- see here: http://stackoverflow.com/questions/27003492/celeryd-with-rabbitmq-hangs-on-mingle-searching-for-neighbors-but-plain-cele/27011229#27011229

RUN mkdir -p /opt/alertsd /opt/plugins

COPY alertsd /opt/alertsd
COPY plugins /opt/plugins
ADD manage.py /opt/
ADD settings.py /opt/
ADD wsgi.py /opt/
ADD urls.py /opt/
ADD start_wsgi.sh /opt/

# Python dependencies:
#
# DjangoRestless/restless -- restless is the rest framework we use in django for the REST api

RUN pip install DjangoRestless restless

# create the database models
RUN cd /opt && \
    python manage.py syncdb --noinput

# set up the db so it can be accessed by both celery workers and the django api
RUN chmod 660 /opt/db.sqlite3 && \
    adduser celery www-data

RUN mkdir /opt/alertsd/run

RUN chown -R www-data:www-data /opt/

# copy the system configs to their proper locations 
# NOTE: this will overwrite existing configs, so doing this if you're using these things for other stuff could be detrimental!
ADD conf/nginx/nginx.conf /etc/nginx/
ADD conf/nginx/alertsd.conf /etc/nginx/conf.d/
ADD conf/supervisor/* /etc/supervisor/conf.d/

EXPOSE 8080

# create the plugin entries
RUN cd /opt && \
    python manage.py syncplugins

# ADD block.sh /usr/local/bin/
# CMD ["/usr/local/bin/block.sh"]

CMD ["supervisord","-nc","/etc/supervisor/supervisord.conf"]

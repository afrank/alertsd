#!/bin/bash

NAME="alertsd"                              #Name of the application (*)
DJANGODIR="/opt"             # Django project directory (*)
SOCKFILE="/opt/alertsd/run/gunicorn.sock"        # we will communicate using this unix socket (*)
USER=www-data                                        # the user to run as (*)
GROUP=www-data                                     # the group to run as (*)
NUM_WORKERS=8                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=wsgi                     # WSGI module name (*)

echo "Starting $NAME as $USER"

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

cd $DJANGODIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec `which gunicorn` ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --settings $DJANGO_SETTINGS_MODULE \
  --bind=unix:$SOCKFILE

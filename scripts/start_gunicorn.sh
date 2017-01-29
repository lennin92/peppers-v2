#!/usr/bin/env bash

LOG_FILE="/var/log/peppers.log"                     # Path to log file
LOG_LEVEL="info"                                    # Log level (info, debig, warning, error, critical)
NAME="peppers"                                      # Name of the application (process name)
DJANGODIR=/home/administrador/peppers-v2/           # Django project directory
BIND_SOCKET="localhost:8787"                        # we will communicte using this socket
USER=administrador                                  # the user to run as
WORKERS=3                                           # how many worker processes should Gunicorn spawn
WORKER_TYPE="gevent"                                # worker type (sync, eventel, gevent, tornado) RECOMENDED: gevent
DJANGO_WSGI_MODULE=peppers.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --worker-class $WORKER_TYPE \
  --user=$USER \
  --bind=$BIND_SOCKET \
  --log-level=$LOG_LEVEL \
  --log-file=$LOG_FILE
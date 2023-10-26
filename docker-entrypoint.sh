#!/bin/bash
set -e

if [ "$1" = "run" ]; then
  exec python /opt/app/manage.py start
elif [ "$1" = "migrate" ]; then
  exec python /opt/app/manage.py migrate
else
  exec "$@"
fi
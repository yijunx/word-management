#! /bin/bash
source ./admin_user.env  # well still need to seed!!
echo starting server
gunicorn app.patched:app -w 1 -k gevent --bind 0.0.0.0:8000
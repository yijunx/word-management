#! /bin/bash
source ./admin_user.env
echo seed words...
python seed_words.py
echo starting server... 3 workers
gunicorn app.patched:app -w 3 -k gevent --bind 0.0.0.0:8000
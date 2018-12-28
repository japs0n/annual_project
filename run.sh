#!/usr/bin/env bash

# run gunicorn service
gunicorn wsgi:app -w 8 -k 'gevent' -b 0.0.0.0:8008 --reload --access-logfile access.log --error-logfile error.log

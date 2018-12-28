#!/usr/bin/env bash

# run gunicorn service
gunicorn wsgi:app -c ./gunicorn.py

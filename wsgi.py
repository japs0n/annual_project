#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import create_app
from flask_cors import CORS
import os

config_name = os.environ.get('FLASK_CONFIG_NAME', 'default')
app = create_app(config_name)
CORS(app, supports_credentials=True)
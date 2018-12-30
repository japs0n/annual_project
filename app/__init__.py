from flask import Flask
from config import config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

# set log handler & format
handler = logging.FileHandler('annual.log', encoding='UTF-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True)
    app.logger.addHandler(handler)
    db.init_app(app)

    from app.api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

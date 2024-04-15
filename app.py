from flask import Flask, Blueprint
from flask_restx import Resource, Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import logging
from logging.config import dictConfig

from routes import api

dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'time-rotate': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': './logs/app.log',
            'when': 'D',
            'interval': 10,
            'backupCount': 5,
            'delay': False,
            'encoding': 'utf-8',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'time-rotate']
    }
})


app = Flask(__name__)
api.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
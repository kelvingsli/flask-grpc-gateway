from flask import Flask
from flask_jwt_extended import JWTManager
import yaml
from logging.config import dictConfig
from datetime import timedelta

from routes import api

# Load YAML file into python config object
with open('config.yaml', 'rt') as f:
    yamlconfig = yaml.safe_load(f.read())

dictConfig(yamlconfig['logging-config'])

app = Flask(__name__)
api.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = yamlconfig['jwt']['secretkey']
app.config["JWT_COOKIE_SECURE"] = yamlconfig['jwt']['cookiesecure']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=yamlconfig['jwt']['expirehours'])

jwt = JWTManager(app)

def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)
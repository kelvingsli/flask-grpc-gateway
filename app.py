from flask import Flask, Blueprint
from flask_restx import Resource, Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from routes import api

app = Flask(__name__)
api.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
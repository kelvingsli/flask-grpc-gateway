from flask import request, Response
from flask_restx import Namespace, Resource, fields, reqparse

class CreateUserReqModel():

    def __init__(self, api):
        self.api = api
        self.create_user_req = api.model('CreateUserReq', {
            'first_name': fields.String(required=True, description='First Name'),
            'last_name': fields.String(required=True, description='Last Name'),
            'email': fields.String(required=True, description='The task unique identifier'),
            'password': fields.String(required=True, description='The task details')
        })

class User():
    id = None
    email = ''
    first_name = ''
    last_name = ''

    def __init__(self, id, email, first_name, last_name):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


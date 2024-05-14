from flask import request, Response
from flask_restx import Namespace, Resource, fields, reqparse

class LoginReqModel():

    def __init__(self, api):
        self.api = api
        self.login_req = api.model('LoginReq', {
            'email': fields.String(required=True, description='The task unique identifier'),
            'password': fields.String(required=True, description='The task details')
        })

class RefreshReqModel():

    def __init__(self, api):
        self.api = api
        self.refresh_req = api.model('RefreshReq', {
            'refresh': fields.String(required=True, description='The task unique identifier')
        })

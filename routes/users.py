from flask import Response, make_response
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
import logging

from main_app.models.userdto import CreateUserReqDto
from main_app.models.api.users import CreateUserReqModel
from main_app.models.api.base_responses import BaseResponse
from main_app.service.UserService import UserService

api = Namespace('users', description='Users related operations')
_logger = logging.getLogger(__name__)
   
@api.route('/')
class BaseUser(Resource):

    @api.doc('list_users')
    @api.doc(security='jwt')
    @jwt_required()
    def get(self):
        _logger.info('Testing...')
        return Response('All Users')

    @api.doc('create_user')
    @api.expect(CreateUserReqModel(api).create_user_req)
    def post(self):
        res = BaseResponse()
        svc = UserService()
        res._response_data = svc.CreateUser(CreateUserReqDto(api.payload['email'], api.payload['first_name'], api.payload['last_name'], api.payload['password']))
        return make_response(res.to_json(), 200)

@api.route('/<userid>')
class GetUser(Resource):

    @api.doc('get_user')
    @api.doc(security='jwt')
    @jwt_required()
    def get(self, userid):
        res = BaseResponse()
        svc = UserService()
        q_userid = int(userid)
        res._response_data = svc.GetUser(q_userid)
        return make_response(res.to_json(), 200)
        
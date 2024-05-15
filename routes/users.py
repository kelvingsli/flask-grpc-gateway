from flask import Response, make_response
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
import logging

from main_app.models.userdto import CreateUserReqDto, UserDto
from main_app.models.api.users import CreateUserReqModel, UpdatePasswordReqModel
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
        res.response_data = svc.GetUser(q_userid)
        return make_response(res.to_json(), 200)

@api.route('/<userid>/password')
class UpdatePassword(Resource):

    @api.doc('update_password')
    @api.doc(security='jwt')
    @api.expect(UpdatePasswordReqModel(api).update_password_req)
    @jwt_required()
    def post(self, userid):
        res = BaseResponse()
        svc = UserService()
        q_userid = int(userid)
        response_data = {}
        data = svc.UpdatePassword(q_userid, api.payload['password'])
        if data.IsSuccess == True:
            response_data['user'] = UserDto(data.User.UserId, data.User.Email, data.User.FirstName, data.User.LastName)
            res.response_data = response_data
            return make_response(res.to_json(), 200)
        else:
            res.error = 'invalid login'
            return make_response(res.to_json(), 401)

from flask import Response, make_response
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required
import logging

from .base_route import BaseRoute
import main_app.grpc.useraccount_pb2 as useraccount_pb2
import main_app.grpc.useraccount_pb2_grpc as useraccount_pb2_grpc
from main_app.models.users import CreateUserReqrModel, User
from main_app.models.base_responses import BaseResponse

api = Namespace('users', description='Users related operations')
_logger = logging.getLogger(__name__)
   
@api.route('/')
class BaseUser(BaseRoute, Resource):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('list_users')
    @api.doc(security='jwt')
    @jwt_required()
    def get(self):
        _logger.info('Testing...')
        return Response('All Users')

    @api.doc('create_user')
    @api.expect(CreateUserReqrModel(api).create_user_req)
    def post(self):
        res = BaseResponse()
        self.stub = useraccount_pb2_grpc.UserAccountStub(self.channel)
        q_email = api.payload['email']
        q_first_name = api.payload['first_name']
        q_last_name = api.payload['last_name']
        q_password = api.payload['password']

        data = self.stub.CreateUser(useraccount_pb2.CreateUserRequest(FirstName=q_first_name, LastName=q_last_name, Email=q_email, Password=q_password))
        res._response_data = User(data.UserId, data.Email, data.FirstName, data.LastName)
        return make_response(res.to_json(), 200)

@api.route('/<userid>')
class GetUser(BaseRoute):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('get_users')
    @api.doc(security='jwt')
    @jwt_required()
    def get(self, userid):
        res = BaseResponse()
        self.stub = useraccount_pb2_grpc.UserAccountStub(self.channel)
        q_userid = int(userid)
        print(q_userid)
        data = self.stub.GetUser(useraccount_pb2.User(UserId=q_userid))
        res._response_data = User(data.UserId, data.Email, data.FirstName, data.LastName)
        return make_response(res.to_json(), 200)
        
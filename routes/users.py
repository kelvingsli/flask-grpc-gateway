from flask import Response, jsonify, make_response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import logging

from .base_route import BaseRoute
import main_app.grpc.useraccount_pb2 as useraccount_pb2
import main_app.grpc.useraccount_pb2_grpc as useraccount_pb2_grpc
from main_app.models.users import UserModel, CreateUserReqrModel, User
from main_app.models.base_responses import BaseResponse

api = Namespace('users', description='Users related operations')
_logger = logging.getLogger(__name__)
   
@api.route('/')
class CreateUser(BaseRoute, Resource):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('list_users')
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

@api.route('/test/<userid>')
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


@api.route('/login/')
class LoginUser(BaseRoute, Resource):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('login_user')
    @api.expect(UserModel(api).login_req)
    def post(self):
        res = BaseResponse()

        try:
            self.stub = useraccount_pb2_grpc.UserAccountStub(self.channel)
            q_email = api.payload['email']
            q_password = api.payload['password']

            data = self.stub.LoginUser(useraccount_pb2.LoginUserRequest(Email=q_email, Password=q_password))
            response_data = {}

            print(f'Login is {data.IsSuccess}')
            if data.IsSuccess == True:
                userData = User(data.User.UserId, data.User.Email, data.User.FirstName, data.User.LastName)
                access_token = create_access_token(identity=userData.id)
                refresh_token = create_refresh_token(identity=userData.id)
                response_data['user'] = User(data.User.UserId, data.User.Email, data.User.FirstName, data.User.LastName)
                response_data['access_token'] = access_token
                response_data['refresh_token'] = refresh_token
                res.response_data = response_data
                return make_response(res.to_json(), 200)
            else:
                res.error = 'invalid login'
                return make_response(res.to_json(), 401)
        except Exception as err:
            _logger.error(err)
            res.error = 'server error'
            return make_response(res.to_json(), 500)

        
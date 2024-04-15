from flask import Response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from .base_route import BaseRoute
import main_app.grpc.useraccount_pb2 as useraccount_pb2
import main_app.grpc.useraccount_pb2_grpc as useraccount_pb2_grpc
from main_app.models.users import UserModel, CreateUserReqrModel, User

api = Namespace('users', description='Users related operations')

   
@api.route('/')
class CreateUser(BaseRoute, Resource):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('list_users')
    def get(self):
        return Response('All Users')

    @api.doc('create_user')
    @api.expect(CreateUserReqrModel(api).create_user_req)
    def post(self):
        self.stub = useraccount_pb2_grpc.UserAccountStub(self.channel)
        q_email = api.payload['email']
        q_first_name = api.payload['first_name']
        q_last_name = api.payload['last_name']
        q_password = api.payload['password']

        data = self.stub.CreateUser(useraccount_pb2.CreateUserRequest(FirstName=q_first_name, LastName=q_last_name, Email=q_email, Password=q_password))
        
        return Response(f'Created User with Id {data.UserId}')

@api.route('/test/<userid>')
class GetUser(BaseRoute):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('get_users')
    @api.doc(security='jwt')
    @jwt_required()
    def get(self, userid):
        self.stub = useraccount_pb2_grpc.UserAccountStub(self.channel)
        q_userid = int(userid)
        print(q_userid)

        data = self.stub.GetUser(useraccount_pb2.User(UserId=q_userid))

        return Response(f'First Name: {data.FirstName} and Id is {data.UserId}')


@api.route('/login/')
class LoginUser(BaseRoute, Resource):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('login_user')
    @api.expect(UserModel(api).login_req)
    def post(self):
        self.stub = useraccount_pb2_grpc.UserAccountStub(self.channel)
        q_email = api.payload['email']
        q_password = api.payload['password']

        data = self.stub.LoginUser(useraccount_pb2.LoginUserRequest(Email=q_email, Password=q_password))
        access_token = ''
        if data.IsSuccess:
            user = User(data.User.UserId, data.User.Email, data.User.FirstName, data.User.LastName)
            access_token = create_access_token(identity=user.id)

        return Response(f'Login is : {data.IsSuccess} and access token is {access_token}')
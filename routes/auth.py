from flask import make_response
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import logging

from .base_route import BaseRoute
import main_app.grpclib.useraccount_pb2 as useraccount_pb2
import main_app.grpclib.useraccount_pb2_grpc as useraccount_pb2_grpc
from main_app.models.users import User
from main_app.models.auth import LoginReqModel
from main_app.models.base_responses import BaseResponse

api = Namespace('auth', description='Authentication related operations')
_logger = logging.getLogger(__name__)
   
@api.route('/login/')
class LoginUser(BaseRoute, Resource):

    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('login_user')
    @api.expect(LoginReqModel(api).login_req)
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

@api.route('/refresh/')
class RefreshToken(BaseRoute, Resource):
    def __init__(self, Resource):
        super().__init__(Resource, api)

    @api.doc('refresh')
    # @api.expect(RefreshReqModel(api).refresh_req)
    @api.doc(security='jwtrefresh')
    @jwt_required(refresh=True)
    def post(self):
        res = BaseResponse()

        try:
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            response_data = {}
            response_data['access_token'] = new_token
            res.response_data = response_data
            return make_response(res.to_json(), 200)
        except Exception as err:
            _logger.error(err)
            res.error = 'server error'
            return make_response(res.to_json(), 500)
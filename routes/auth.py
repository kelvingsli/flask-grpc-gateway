from flask import make_response
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import logging

from main_app.models.userdto import UserDto
from main_app.models.api.auth import LoginReqModel
from main_app.models.api.base_responses import BaseResponse
from main_app.service.UserService import UserService

api = Namespace('auth', description='Authentication related operations')
_logger = logging.getLogger(__name__)
   
@api.route('/login/')
class LoginUser(Resource):

    @api.doc('login_user')
    @api.expect(LoginReqModel(api).login_req)
    def post(self):
        res = BaseResponse()
        svc = UserService()

        try:
            q_email = api.payload['email']
            q_password = api.payload['password']
            data = svc.LoginUser(q_email, q_password)
            response_data = {}

            _logger.info(f'Login is {data.IsSuccess}')
            if data.IsSuccess == True:
                userData = UserDto(data.User.UserId, data.User.Email, data.User.FirstName, data.User.LastName)
                access_token = create_access_token(identity=userData.id)
                refresh_token = create_refresh_token(identity=userData.id)
                response_data['user'] = UserDto(data.User.UserId, data.User.Email, data.User.FirstName, data.User.LastName)
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
class RefreshToken(Resource):

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
from main_app.models.userdto import UserDto
from .BaseGrpcService import BaseGrpcService
import main_app.grpclib.useraccount_pb2 as useraccount_pb2

class UserService(BaseGrpcService):

    def CreateUser(self, req):
        g_res = self.stub.CreateUser(useraccount_pb2.CreateUserRequest(FirstName=req.first_name, LastName=req.last_name, Email=req.email, Password=req.password))
        return UserDto(g_res.UserId, g_res.Email, g_res.FirstName, g_res.LastName)
    
    def GetUser(self, user_id):
        g_res = self.stub.GetUser(useraccount_pb2.User(UserId=user_id))
        return UserDto(g_res.UserId, g_res.Email, g_res.FirstName, g_res.LastName)
    
    def LoginUser(self, email, password):
        g_res = self.stub.LoginUser(useraccount_pb2.LoginUserRequest(Email=email, Password=password))
        return g_res
    
    def UpdatePassword(self, user_id, password):
        g_res = self.stub.UpdatePassword(useraccount_pb2.UpdatePasswordRequest(UserId=user_id, Password=password))
        return g_res
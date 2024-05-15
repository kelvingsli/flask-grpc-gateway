from flask_restx import Namespace, Resource, fields

from main_app.grpclib.grpc_channel import HrbGrpcChannel
from main_app.grpclib import useraccount_pb2_grpc

class BaseRoute(Resource):
    def __init__(self, Resource, api):
        self.api = api
        grpc_conn = HrbGrpcChannel()
        self.channel = grpc_conn.channel
        self.stub = useraccount_pb2_grpc.UserAccountStub(grpc_conn.channel)
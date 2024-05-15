from main_app.grpclib.grpc_channel import HrbGrpcChannel
from main_app.grpclib import useraccount_pb2_grpc

class BaseGrpcService():
    def __init__(self):
        grpc_conn = HrbGrpcChannel()
        self.channel = grpc_conn.channel
        self.stub = useraccount_pb2_grpc.UserAccountStub(grpc_conn.channel)
import grpc

class HrbGrpcChannel():
    def __init__(self):
        if not hasattr(self, 'channel'):
            self.channel = grpc.insecure_channel('localhost:50051')
        

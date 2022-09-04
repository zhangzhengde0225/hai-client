from .grpc_secure_client import HAIGrpcClient
from .hubs import HAIHub

class HAIClient(HAIGrpcClient):
    def __init__(self, ip='localhost', port=50052):
        super().__init__(ip, port)
        self.hub = HAIHub(haic=self)

        


    

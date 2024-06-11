from concurrent import futures
import grpc
import storage_pb2
import storage_pb2_grpc

class StorageNode(storage_pb2_grpc.StorageServicer):
    def __init__(self):
        self.chunks = {}

    def StoreChunk(self, request, context):
        self.chunks[request.chunk_id] = request.chunk_data
        return storage_pb2.StoreResponse(status='success')

    def RetrieveChunk(self, request, context):
        chunk_data = self.chunks.get(request.chunk_id, b'')
        return storage_pb2.RetrieveResponse(chunk_data=chunk_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_pb2_grpc.add_StorageServicer_to_server(StorageNode(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

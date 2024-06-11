from concurrent import futures
import grpc
import file_system_pb2
import file_system_pb2_grpc
import os
import hashlib

class MasterNode(file_system_pb2_grpc.FileSystemServicer):
    def __init__(self):
        self.metadata = {}

    def split_into_chunks(self, file_data):
        chunk_size = 1024 * 1024  # 1MB chunks
        return [file_data[i:i + chunk_size] for i in range(0, len(file_data), chunk_size)]

    def generate_chunk_id(self, chunk_data):
        return hashlib.sha256(chunk_data).hexdigest()

    def distribute_chunks(self, chunk_data):
        # Dummy implementation: Distribute to two storage nodes
        return ["storage_node_1", "storage_node_2"]

    def UploadFile(self, request, context):
        chunks = self.split_into_chunks(request.file_data)
        chunk_ids = []
        for chunk in chunks:
            chunk_id = self.generate_chunk_id(chunk)
            chunk_ids.append(chunk_id)
            self.metadata[chunk_id] = {
                'locations': self.distribute_chunks(chunk)
            }
        return file_system_pb2.UploadResponse(chunk_ids=chunk_ids)

    def DownloadFile(self, request, context):
        locations = [file_system_pb2.ChunkLocation(chunk_id=chunk_id, storage_nodes=self.metadata[chunk_id]['locations']) for chunk_id in request.chunk_ids]
        return file_system_pb2.DownloadResponse(locations=locations)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_system_pb2_grpc.add_FileSystemServicer_to_server(MasterNode(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

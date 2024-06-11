import grpc
import file_system_pb2
import file_system_pb2_grpc

def upload_file(file_name, file_path):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_system_pb2_grpc.FileSystemStub(channel)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        response = stub.UploadFile(file_system_pb2.UploadRequest(file_name=file_name, file_data=file_data))
        print(f'File uploaded with chunk IDs: {response.chunk_ids}')

def download_file(chunk_ids):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_system_pb2_grpc.FileSystemStub(channel)
        response = stub.DownloadFile(file_system_pb2.DownloadRequest(chunk_ids=chunk_ids))
        for location in response.locations:
            print(f'Chunk ID: {location.chunk_id}, Storage Nodes: {location.storage_nodes}')

if __name__ == '__main__':
    # Example usage
    upload_file('example.txt', 'path/to/example.txt')
    chunk_ids = ['chunk_id_1', 'chunk_id_2']  # Example chunk IDs
    download_file(chunk_ids)

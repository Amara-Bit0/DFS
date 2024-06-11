import sys
import grpc
import file_system_pb2
import file_system_pb2_grpc

def get_file_system_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return file_system_pb2_grpc.FileSystemStub(channel)

def create_file(file_name, data):
    stub = get_file_system_stub()
    chunks = []
    chunk_size = 1024 * 1024  # 1 MB
    for i in range(0, len(data), chunk_size):
        chunk_data = data[i:i + chunk_size]
        chunks.append(file_system_pb2.FileChunk(file_name=file_name, chunk_id=i//chunk_size, data=chunk_data))
    response = stub.StoreFile(file_system_pb2.FileChunks(chunks=chunks))
    print(response.message)

def read_file(file_name):
    stub = get_file_system_stub()
    response = stub.RetrieveFile(file_system_pb2.FileRequest(file_name=file_name))
    file_data = b''.join(chunk.data for chunk in response.chunks)
    print(file_data.decode())

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python cli.py create_file <filename> <data>")
        print("  python cli.py read_file <filename>")
        sys.exit(1)

    command = sys.argv[1]
    file_name = sys.argv[2]

    if command == 'create_file':
        data = sys.argv[3] if len(sys.argv) > 3 else ""
        create_file(file_name, data.encode())
    elif command == 'read_file':
        read_file(file_name)
    else:
        print("Unknown command:", command)
        sys.exit(1)

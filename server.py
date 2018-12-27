#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from pathlib import Path
from concurrent import futures
from rpc import data_pb2, data_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8080'

CHUNK_SIZE = 1024 * 1024

DIR = 'g:/dfs-test/server1/'

class FileServer(data_pb2_grpc.FileSystemServicer):

    def CreateFile(self, request, context):
        file_path = DIR + request.filename
        file = Path(file_path)
        if file.is_file():
            return data_pb2.Response(code=1, message='File already exists.')
        else:
            f = open(file_path, 'w')
            f.close()
            return data_pb2.Response(code=0, message='Success.')

    def DeleteFile(self, request, context):
        file_path = DIR + request.filename
        file = Path(file_path)
        if not file.is_file():
            return data_pb2.Response(code=1, message='File not exists.')
        else:
            file.unlink()
            return data_pb2.Response(code=0, message='Success.')

    def ListFiles(self, requset, context):
        for file in Path(DIR).iterdir():
            if file.is_file():
                info = file.stat()
                yield data_pb2.FileList(filename=file.name,
                                        size=info.st_size,
                                        createdtime=info.st_ctime,
                                        modifiedtime=info.st_mtime)

    # def Upload(self, request_iterator, context):
    #     file_path = DIR + 'test.png'
    #     with open(file_path, 'wb') as f:
    #         for chunk in request_iterator:
    #             f.write(chunk.buffer)
    #     return data_pb2.UploadStatusCode(code=1)

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    data_pb2_grpc.add_FileSystemServicer_to_server(FileServer(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()

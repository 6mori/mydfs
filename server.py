#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from pathlib import Path
from concurrent import futures
from rpc import data_pb2, data_pb2_grpc

# from portalocker.portalocker import lock, unlock
# from portalocker.constants import LOCK_SH, LOCK_EX, LOCK_NB, LOCK_UN

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8080'

CHUNK_SIZE = 1024 * 1024

DIR = 'g:/dfs-test/server1/'

class FileServer(data_pb2_grpc.FileSystemServicer):
    locked_files = []

    def checkIfLocked(self, filename):
        if filename in self.locked_files:
            return True
        else:
            return False

    def Lock(self, request, context):
        file_path = DIR + request.filename
        if self.checkIfLocked(file_path):
            return data_pb2.Response(code=1, message='File was locked by others.')
        else:
            self.locked_files.append(file_path)
            return data_pb2.Response(code=0, message='Locked.')

    def Unlock(self, request, context):
        file_path = DIR + request.filename
        if self.checkIfLocked(file_path):
            self.locked_files.remove(file_path)
        return data_pb2.Response(code=0, message='Unlocked.')

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

    def Download(self, request, context):
        file_path = DIR + request.filename
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield data_pb2.Chunk(buffer=chunk)

    def Upload(self, request_iterator, context):
        for no, request in enumerate(request_iterator):
            if no == 0:
                file_path = DIR + request.filename
                file = open(file_path, 'wb')
            else:
                file.write(request.buffer)
        file.close()
        return data_pb2.Response(code=0, message='ok')




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

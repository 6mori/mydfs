#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
from datetime import datetime
from rpc import data_pb2, data_pb2_grpc

_HOST = 'localhost'
_PORT = '8080'

CHUNK_SIZE = 1024 * 1024

# def ReadFile(filename):
#     with open(filename, 'rb') as f:
#         while True:
#             chunk = f.read(CHUNK_SIZE)
#             if len(chunk) == 0:
#                 return
#             yield data_pb2.Chunk(buffer=chunk)
class FileSystemClient():
    def __init__(self):
        channel = grpc.insecure_channel(_HOST + ':' + _PORT)
        self.stub = data_pb2_grpc.FileSystemStub(channel=channel)

    def CreateFile(self, filename):
        response = self.stub.CreateFile(data_pb2.Filename(filename=filename))
        print(response.code, response.message)

    def ListFiles(self):
        for response in self.stub.ListFiles(data_pb2.Empty()):
            print(response.filename, response.size, datetime.fromtimestamp(response.createdtime), datetime.fromtimestamp(response.modifiedtime))

    

if __name__ == '__main__':
    client = FileSystemClient()
    client.ListFiles()
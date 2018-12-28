#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from pathlib import Path
import subprocess 

import grpc
from rpc import data_pb2, data_pb2_grpc

_HOST = 'localhost'
_PORT = '8080'

CHUNK_SIZE = 1024 * 1024

DIR = 'g:/dfs-test/client1/'


class FileSystemClient():
    def __init__(self):
        channel = grpc.insecure_channel(_HOST + ':' + _PORT)
        self.stub = data_pb2_grpc.FileSystemStub(channel=channel)

    def CreateFile(self, filename):
        response = self.stub.CreateFile(data_pb2.Filename(filename=filename))
        print(response.code, response.message)

    def DeleteFile(self, filename):
        while not self.LockFile(filename):
            time.sleep(2)
        response = self.stub.DeleteFile(data_pb2.Filename(filename=filename))
        self.UnlockFile(filename)
        print(response.code, response.message)

    def ListFiles(self):
        for response in self.stub.ListFiles(data_pb2.Empty()):
            print(response.filename, response.size, datetime.fromtimestamp(response.createdtime), datetime.fromtimestamp(response.modifiedtime))

    def OpenFile(self, filename):
        file_path = DIR + 'tmp_' + filename
        if Path(file_path).is_file():
            print('Already in cache.')
        else:
            while not self.LockFile(filename):
                time.sleep(2)
            result = self._Download(filename, file_path)
            self.UnlockFile(filename)
        os.chmod(file_path, S_IREAD|S_IRGRP|S_IROTH)
        os.system(file_path)

    def UpdateFile(self, filename):
        file_path = DIR + 'tmp_' + filename
        while not self.LockFile(filename):
            time.sleep(2)
        if Path(file_path).is_file():
            print('Already in cache.')
        else:
            result = self._Download(filename, file_path)
        os.chmod(file_path, S_IWUSR|S_IREAD)
        os.system(file_path)
        response = self._Upload(filename, file_path)
        print(response.code, response.message)
        self.UnlockFile(filename)

    def LockFile(self, filename):
        response = self.stub.Lock(data_pb2.Filename(filename=filename))
        # print(response.code, response.message)
        if response.code == 0:
            return True
        else:
            return False

    def UnlockFile(self, filename):
        response = self.stub.Unlock(data_pb2.Filename(filename=filename))
        print(response.code, response.message)
        if response.code == 0:
            return True
        else:
            return False
        
    def _ReadFile(self, filename, fullpath):
        yield data_pb2.UploadRequest(filename=filename)
        with open(fullpath, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield data_pb2.UploadRequest(buffer=chunk)

    def _Upload(self, filename, fullpath):
        return self.stub.Upload(self._ReadFile(filename, fullpath))

    def _Download(self, filename, fullpath):
        with open(fullpath, 'wb') as f:
            for chunk in self.stub.Download(data_pb2.Filename(filename=filename)):
                f.write(chunk.buffer)
        return 0
    

if __name__ == '__main__':
    client = FileSystemClient()
    # if client.LockFile('a.txt'):
    client.DeleteFile('b')
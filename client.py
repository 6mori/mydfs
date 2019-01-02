#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
from datetime import datetime
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from pathlib import Path
import subprocess 

import grpc
from rpc import data_pb2, data_pb2_grpc

_TRACKER_HOST = 'localhost'
_TRACKER_PORT = '8081'

CHUNK_SIZE = 1024 * 1024

DIR = 'g:/dfs-test/client1/'


class FileSystemClient():
    def __init__(self, uid=0):
        channel = grpc.insecure_channel(_TRACKER_HOST + ':' + _TRACKER_PORT)
        self.tracker_stub = data_pb2_grpc.TrackerStub(channel=channel)
        self.user_id = int(uid)

    # def CreateFile(self, filename):
    #     response = self.stub.CreateFile(data_pb2.Filename(filename=filename))
    #     print(response.code, response.message)

    def DeleteFile(self, filename):
        server_address = self.GetHost(filename)
        channel = grpc.insecure_channel(server_address)
        self.server_stub = data_pb2_grpc.FileSystemStub(channel=channel)
        while not self.LockFile(filename):
            time.sleep(2)
        response = self.server_stub.DeleteFile(data_pb2.Filename(filename=filename))
        self.UnlockFile(filename)
        self.tracker_stub.DeleteFile(data_pb2.Filename(filename=filename))
        file_path = DIR + 'tmp_' + filename
        if Path(file_path).is_file():
            os.chmod(file_path, S_IWUSR|S_IREAD)
            Path(file_path).unlink()
        print(response.code, response.message)

    def ListFiles(self):
        for response in self.tracker_stub.ListFiles(data_pb2.Empty()):
            print(response.filename, response.size, \
                datetime.fromtimestamp(response.createdtime), \
                datetime.fromtimestamp(response.modifiedtime))

    def GetHost(self, filename):
        response = self.tracker_stub.GetHost(data_pb2.Filename(filename=filename))
        while response.code != 0:
            print('Servers are all down. Try again.')
            time.sleep(2)
            response = self.tracker_stub.GetHost(data_pb2.Filename(filename=filename))
        return response.address

    def OpenFile(self, filename):
        response = self.tracker_stub.GetServer(data_pb2.Filename(filename=filename))
        if response.code != 0:
            response = self.tracker_stub.GetHost(data_pb2.Filename(filename=filename))
        channel = grpc.insecure_channel(response.address)
        self.server_stub = data_pb2_grpc.FileSystemStub(channel=channel)
        file_path = DIR + 'tmp_' + filename
        if self.__CheckCache(filename, file_path):
            print('Already in cache.')
        else:
            time.sleep(5)
            while not self.LockFile(filename):
                time.sleep(2)
            result = self.__Download(filename, file_path)
            self.UnlockFile(filename)
        os.chmod(file_path, S_IREAD|S_IRGRP|S_IROTH)
        os.system(file_path)
        os.chmod(file_path, S_IWUSR|S_IREAD)

    def UpdateFile(self, filename):
        server_address = self.GetHost(filename)
        channel = grpc.insecure_channel(server_address)
        self.server_stub = data_pb2_grpc.FileSystemStub(channel=channel)
        file_path = DIR + 'tmp_' + filename
        while not self.LockFile(filename):
            time.sleep(2)
        if self.__CheckCache(filename, file_path):
            print('Already in cache.')
        else:
            result = self.__Download(filename, file_path)
        os.chmod(file_path, S_IWUSR|S_IREAD)
        os.system(file_path)
        response = self.__Upload(filename, file_path)
        print(response.code, response.message)
        self.UnlockFile(filename)

    def LockFile(self, filename):
        response = self.server_stub.Lock(data_pb2.LockRequest(filename=filename, userid=self.user_id))
        # print(response.code, response.message)
        if response.code == 0:
            return True
        else:
            return False

    def UnlockFile(self, filename):
        response = self.server_stub.Unlock(data_pb2.LockRequest(filename=filename, userid=self.user_id))
        print(response.code, response.message)
        if response.code == 0:
            return True
        else:
            return False

    def __CheckCache(self, filename, fullpath):
        if Path(fullpath).is_file():
            remote_file_info = self.server_stub.GetFileInfo(data_pb2.Filename(filename=filename))
            if Path(fullpath).stat().st_mtime >= remote_file_info.modifiedtime:
                return True
        return False
        
    def __ReadFile(self, filename, fullpath):
        yield data_pb2.UploadRequest(filename=filename)
        with open(fullpath, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield data_pb2.UploadRequest(buffer=chunk)

    def __Upload(self, filename, fullpath):
        return self.server_stub.Upload(self.__ReadFile(filename, fullpath))

    def __Download(self, filename, fullpath):
        with open(fullpath, 'wb') as f:
            for chunk in self.server_stub.Download(data_pb2.Filename(filename=filename)):
                f.write(chunk.buffer)
        return 0
    

if __name__ == '__main__':
    DIR = sys.argv[2]
    client = FileSystemClient(sys.argv[1])
    client.UpdateFile('test.txt')
    client.OpenFile('test.txt')
    # client.DeleteFile('test.txt')
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import grpc
import time
import json
from pathlib import Path
from concurrent import futures
from rpc import data_pb2, data_pb2_grpc

# from portalocker.portalocker import lock, unlock
# from portalocker.constants import LOCK_SH, LOCK_EX, LOCK_NB, LOCK_UN

_HEARTBEAT_SECONDS = 2
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = ''

_TRACKER_HOST = 'localhost'
_TRACKER_PORT = '8081'

CHUNK_SIZE = 1024 * 1024

_DIR = ''

class FileServer(data_pb2_grpc.FileSystemServicer):

    def __init__(self):
        channel = grpc.insecure_channel(_TRACKER_HOST + ':' + _TRACKER_PORT)
        self.tracker_stub = data_pb2_grpc.TrackerStub(channel=channel)
        self.address = _HOST + ':' + _PORT
        # self.lock_path = _DIR + 'lock.json'
        self.uncomplete = []
        self.locked_files = {}

    def checkIfLocked(self, filename):
        if filename in self.locked_files:
            return True
        else:
            return False

    def Lock(self, request, context):
        # file_path = _DIR + request.filename
        filename = request.filename
        uid = request.userid
        self.locked_files = self.__ReadData('lock.json')
        if self.checkIfLocked(filename) and self.locked_files[filename] != uid:
            return data_pb2.Response(code=1, message='File was locked by others.')
        else:
            self.locked_files[filename] = uid
            self.__WriteData('lock.json', self.locked_files)
            return data_pb2.Response(code=0, message='Locked.')

    def Unlock(self, request, context):
        filename = request.filename
        uid = request.userid
        self.locked_files = self.__ReadData('lock.json')
        if self.checkIfLocked(filename) and self.locked_files[filename] == uid:
            self.locked_files.pop(filename)
            self.__WriteData('lock.json', self.locked_files)
            return data_pb2.Response(code=0, message='Unlocked.')
        return data_pb2.Response(code=1, message='Permission denied.')

    def CreateFile(self, request, context):
        filename = request.filename
        file_path = _DIR + filename
        # file = Path(file_path)
        f = open(file_path, 'w')
        f.close()
        for no, response in enumerate(self.tracker_stub.GetServers(data_pb2.Filename(filename=filename))):
            address = response.address
            if no == 0 and address != self.address:
                break
            if no == 0 and address == self.address:
                continue
            try:
                self.CreateSlave(filename, address)
            except:
                self.AddUncomplete('create', filename, address)
        return data_pb2.Response(code=0, message='Success.')

    def DeleteFile(self, request, context):
        filename = request.filename
        file_path = _DIR + filename
        file = Path(file_path)
        if not file.is_file():
            return data_pb2.Response(code=1, message='File not exists.')
        else:
            file.unlink()
            for no, response in enumerate(self.tracker_stub.GetServers(data_pb2.Filename(filename=filename))):
                address = response.address
                if no == 0 and address != self.address:
                    break
                if no == 0 and address == self.address:
                    continue
                try:
                    self.DeleteSlave(filename, address)
                except:
                    self.AddUncomplete('delete', filename, address)
            return data_pb2.Response(code=0, message='Success.')

    # def ListFiles(self, requset, context):
    #     for file in Path(_DIR).iterdir():
    #         if file.is_file():
    #             info = file.stat()
    #             yield data_pb2.FileList(filename=file.name,
    #                                     size=info.st_size,
    #                                     createdtime=info.st_ctime,
    #                                     modifiedtime=info.st_mtime)
    def GetFileInfo(self, request, context):
        file_path = _DIR + request.filename
        file = Path(file_path)
        info = file.stat()
        return data_pb2.FileInfo(filename=request.filename,
                                size=info.st_size,
                                createdtime=info.st_ctime,
                                modifiedtime=info.st_mtime)

    def Download(self, request, context):
        file_path = _DIR + request.filename
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield data_pb2.Chunk(buffer=chunk)

    def Upload(self, request_iterator, context):
        for no, request in enumerate(request_iterator):
            if no == 0:
                filename = request.filename
                file_path = _DIR + filename
                file = open(file_path, 'wb')
            else:
                file.write(request.buffer)
        file.close()
        for no, response in enumerate(self.tracker_stub.GetServers(data_pb2.Filename(filename=filename))):
            address = response.address
            if no == 0 and address != self.address:
                break
            if no == 0 and address == self.address:
                continue
            try:
                self.UpdateSlave(filename, address)
            except:
                self.AddUncomplete('update', filename, address)
        return data_pb2.Response(code=0, message='ok')

    def CreateSlave(self, filename, address):
        channel = grpc.insecure_channel(address)
        stub = data_pb2_grpc.FileSystemStub(channel=channel)
        stub.CreateFile(data_pb2.Filename(filename=filename))
    
    def DeleteSlave(self, filename, address):
        channel = grpc.insecure_channel(address)
        stub = data_pb2_grpc.FileSystemStub(channel=channel)
        stub.DeleteFile(data_pb2.Filename(filename=filename))
    
    def UpdateSlave(self, filename, address):
        file_path = _DIR + filename
        channel = grpc.insecure_channel(address)
        stub = data_pb2_grpc.FileSystemStub(channel=channel)
        stub.Upload(self.__ReadFile(filename, file_path))

    def AddUncomplete(self, job, filename, address):
        self.uncomplete = self.__ReadData('uncomplete.json')
        if [job, filename, address] not in self.uncomplete:
            self.uncomplete.append([job, filename, address])
        self.__WriteData('uncomplete.json', self.uncomplete)
    
    def DelUncomplete(self, job, filename, address):
        self.uncomplete = self.__ReadData('uncomplete.json')
        self.uncomplete.remove([job, filename, address])
        self.__WriteData('uncomplete.json', self.uncomplete)
    
    def TryComplete(self):
        self.uncomplete = self.__ReadData('uncomplete.json')
        for job, filename, address in self.uncomplete[:]:
            if job == 'create':
                try:
                    self.CreateSlave(filename, address)
                except:
                    pass
                else:
                    self.DelUncomplete(job, filename, address)
            elif job == 'update':
                try:
                    self.UpdateSlave(filename, address)
                except:
                    pass
                else:
                    self.DelUncomplete(job, filename, address)
            elif job == 'delete':
                try:
                    self.DeleteSlave(filename, address)
                except:
                    pass
                else:
                    self.DelUncomplete(job, filename, address)

    def __ReadFile(self, filename, fullpath):
        yield data_pb2.UploadRequest(filename=filename)
        with open(fullpath, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield data_pb2.UploadRequest(buffer=chunk)
    
    def __ReadData(self, datafile):
        if not Path(_DIR + datafile).is_file():
            if datafile == 'lock.json':
                pedding = {}
            else:
                pedding = []
            with open(_DIR + datafile, 'w') as file:
                json.dump(pedding, file)
            return pedding
        with open(_DIR + datafile, 'r') as file:
            return json.load(file)

    def __WriteData(self, datafile, data):
        with open(_DIR + datafile, 'w') as file:
            json.dump(data, file)



def serve():
    server = FileServer()

    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    data_pb2_grpc.add_FileSystemServicer_to_server(server, grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            server.tracker_stub.HeartBeat(data_pb2.Address(address=_HOST + ':' + _PORT))
            server.TryComplete()
            time.sleep(_HEARTBEAT_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    _PORT = sys.argv[1]
    _DIR = sys.argv[2]
    serve()

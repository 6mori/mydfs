# -*- coding: utf-8 -*-

import random
import json
import grpc
import time
from pathlib import Path
from concurrent import futures
from rpc import data_pb2, data_pb2_grpc

_HEARTBEAT_SECONDS = 5
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8081'

_DIR = 'g:/dfs-test/tracker/'

class Tracker(data_pb2_grpc.TrackerServicer):
    running_server = {}

    def HeartBeat(self, request, context):
        self.running_server[request.address] = True
        return data_pb2.Empty()

    def CheckServer(self):
        for address in list(self.running_server):
            if self.running_server[address] == True:
                self.running_server[address] = False
            else:
                self.running_server.pop(address)
                # self.__RemoveNotAlive(address)

    def ListFiles(self, request, context):
        data = self.__ReadData()
        for filename in data:
            addresses = data[filename]
            channel = grpc.insecure_channel(addresses[0])
            stub = data_pb2_grpc.FileSystemStub(channel=channel)
            file_info = stub.GetFileInfo(data_pb2.Filename(filename=filename))
            yield file_info

    def GetHost(self, request, context):
        data = self.__ReadData()
        filename = request.filename
        if filename not in data:
            servers = list(self.running_server)
            random.shuffle(servers)
            addresses = data[filename] = servers[:2]
            self.__WriteData(data)
            self.__CreateFile(filename, addresses[0])
            return data_pb2.HostAddress(code=0, address=addresses[0])
        else:
            addresses = data[filename]
            host = None
            for index, address in enumerate(addresses):
                if address in self.running_server:
                    host = address
                    addresses[index], addresses[0] = addresses[0], addresses[index]
                    break
            if host:
                self.__WriteData(data)
                return data_pb2.HostAddress(code=0, address=host)
            else:
                return data_pb2.HostAddress(code=1, address=addresses[0])
    
    def GetServers(self, request, context):
        data = self.__ReadData()
        filename = request.filename
        for address in data[filename]:
            yield data_pb2.Address(address=address)
    
    def DeleteFile(self, request, context):
        data = self.__ReadData()
        data.pop(request.filename)
        self.__WriteData(data)
        return data_pb2.Response(code=0, message='Done.')
                
    # def __RemoveNotAlive(self, address):
    #     data = self.__ReadData()
    #     for filename in data:
    #         if address in data[filename]:
    #             data[filename].remove(address)
    #     self.__WriteData(data)

    # def __DeleteFile(self, filename, address):
    #     channel = grpc.insecure_channel(address)
    #     stub = data_pb2_grpc.FileSystemStub(channel=channel)
    #     lock_response = stub.Lock(data_pb2.Filename(filename=filename))
    #     if lock_response.code != 0:
    #         lock_response = stub.Lock(data_pb2.Filename(filename=filename))
    #     result = stub.DeleteFile(data_pb2.Filename(filename=filename))
    #     stub.Unlock(data_pb2.Filename(filename=filename))
    #     print(result.code, result.message)

    def __CreateFile(self, filename, address):
        channel = grpc.insecure_channel(address)
        stub = data_pb2_grpc.FileSystemStub(channel=channel)
        response = stub.CreateFile(data_pb2.Filename(filename=filename))
        print(response.code, response.message)

    def __ReadData(self):
        if not Path(_DIR + 'tracker.json').is_file():
            with open(_DIR + 'tracker.json', 'w') as file:
                json.dump({}, file)
            return {}
        with open(_DIR + 'tracker.json', 'r') as file:
            return json.load(file)

    def __WriteData(self, data):
        with open(_DIR + 'tracker.json', 'w') as file:
            json.dump(data, file)


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    tracker = Tracker()
    data_pb2_grpc.add_TrackerServicer_to_server(tracker, grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            tracker.CheckServer()
            print(tracker.running_server)
            time.sleep(_HEARTBEAT_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()

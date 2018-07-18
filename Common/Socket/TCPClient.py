# -*- coding:utf-8 -*-

from socket import *
from struct import *
from threading import *
from Common.Socket import Packet
import json

class TCPClient:
    def __init__(self,name='gyb333',HOST='127.0.0.1',PORT=8888):
        self.__host=HOST
        self.__port=PORT
        self.__name=name
        self.__recvTo=None

    @property
    def RecvTo(self):
        return self.__recvTo
    @RecvTo.setter
    def RecvTo(self,value):
        self.__recvTo=value

    def Connect(self):
        self.__socket=socket(AF_INET,SOCK_STREAM)
        self.__conn=self.__socket.connect((self.__host,self.__port))
        print("Connect %s:%d OK"%(self.__socket.getsockname()))

    def SendMsg(self):
        key={"Name":self.__name,"RecvTo":self.__recvTo,"Data":"你好，很高兴见到你！"}
        js=json.dumps(key)
        #print(json.loads(js))
        Packet.SendMsg(js.encode(), self.__socket)
        while True:
            cmd = input(">>:").strip()
            if not cmd: continue
            print("发送信息：%s" % cmd)
            Packet.SendMsg(cmd.encode(), self.__socket)

    def RecvMsg(self):
        while True:
            recvData = Packet.RecvMsg(self.__socket)
            if not recvData: break
            print("接收到：%s" % recvData.decode())

    def Close(self):
        if  self.__socket:
            self.__socket.close()

    def Start(self):
        self.Connect()
        Thread(target=self.SendMsg).start()
        self.RecvMsg()
        self.Close()


def main():
    # l = []
    # for i in range(10):
    #     client=TCPClient()
    #     l.append(client)

    client=TCPClient()
    client.Start()
if __name__ == '__main__':
    main()
#-*- coding:utf-8 -*-

from socket import *

class UdpServer:
    def __init__(self,host='127.0.0.1',port=7777):
        self.__host=host
        self.__port=port

    def start(self):
        udpServer=socket(AF_INET,SOCK_DGRAM)
        udpServer.bind((self.__host,self.__port))
        while True:
            data,addr=udpServer.recvfrom(1024)#接收数据
            print("接收到数据:%s from %s"%(data.decode(),addr))

            udpServer.sendto(data.upper(),addr)#发送数据
        udpServer.close()

def main():
    UdpServer().start()

if __name__ == '__main__':
    main()
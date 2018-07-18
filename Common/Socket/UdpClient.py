#-*- coding:utf-8 -*-

from socket import  *

class UdpClient:
    def __init__(self,host='127.0.0.1',port=7777):
        self.__host=host
        self.__port=port

    def Start(self):
        addr=(self.__host,self.__port)
        udpClient=socket(AF_INET,SOCK_DGRAM)
        while True:
            msg=input('>>:').strip()
            if not msg: continue

            udpClient.sendto(msg.encode(),addr) #发送数据

            res,sAddr=udpClient.recvfrom(1024)
            print("从%s接收到数据%s"%(sAddr,res.decode()))

        udpClient.close()


def main():
    UdpClient().Start()

if __name__ == '__main__':
    main()
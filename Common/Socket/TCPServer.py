# -*- coding:utf-8 -*-

from socket import *
from random import *
from time import *
from datetime import datetime
from Common.Socket import Packet
from threading import *
import  json
class TCPServer:
    def __init__(self,HOST='127.0.0.1',PORT=8888):
        self.__host=HOST
        self.__port=PORT

    def start(self):
        s =socket(AF_INET,SOCK_STREAM) #套接字
        s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#解决端口占用
        s.bind((self.__host,self.__port))
        s.listen(2)

        while True:
            conn, addr = s.accept()
            print('客户端%s 连接成功!' % str(addr))
            Thread(target=self.RecvMsg,args=(conn,)).start()
            Thread(target=self.SendMsg, args=(conn,)).start()

        s.close()

    def SendMsg(self,conn,Message="Hello world!"):
        i=1;
        while True:
            try:
                sleep(randint(1,5))
                Message +=str(i);
                i+=1
                Packet.SendMsg(Message.encode(), conn)
            except OSError:
                pass


    def RecvMsg(self,conn):
        try:
            bFirst=True
            while True:  # 通信循环
                recvData = Packet.RecvMsg(conn)
                if not recvData:break
                recvData = recvData.decode()
                if bFirst:
                    bFirst=False
                    js=json.loads(recvData)
                    recvFrom =js["Name"]
                    recvTo=js["RecvTo"]
                    recvData=js["Data"]
                if  recvTo is None:
                    dt = datetime.now()
                    print("%s 接收到客户端%s消息：%s" % (dt,recvFrom, recvData))



        except ConnectionResetError:
            pass
        finally:
            if conn:
                conn.close()




def main():
    s =TCPServer()
    s.start()


if __name__ == '__main__':
    main()


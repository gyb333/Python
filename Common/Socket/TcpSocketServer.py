# -*- coding:utf-8 -*-



from socketserver import *
from time import ctime

class TcpSocketServer(StreamRequestHandler):
    def handle(self):

        self.wfile.write('客户端%s:%s 在%s 连接成功！ '%(self.client_address[0],self.client_address[1],ctime()))
        while True:
            data=self.request.recv(1024)
            if not data: break
            print("接收到客户端%s数据：%s"%(self.client_address,data))
            self.request.send(data.upper())

    @staticmethod
    def Start( host = '127.0.0.1',port = 8888):
        addr = (host, port)
        server = ThreadingTCPServer(addr,TcpSocketServer)
        server.serve_forever()

def main():
    TcpSocketServer.Start()

if __name__ == '__main__':
    main()


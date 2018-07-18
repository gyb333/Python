# -*- coding:utf-8 -*-

from struct import *


def SendMsg(Message,conn):
    # 先发报文头
    header = pack('i', len(Message))
    conn.send(header)
    conn.send(Message)

def RecvMsg(conn):
    #先接收报文头
    header=conn.recv(4)    #4个字节
    unpackResult=unpack('i',header)
    totalSize=unpackResult[0]

    #接收数据
    recvSize=0
    totalData=b''
    while recvSize<totalSize:
        recvData = conn.recv(1024)
        recvSize+=len(recvData)
        totalData+=recvData
    return  totalData




# 每当一个子例程被调用，都有一个“栈帧”被建立，这是用来保存变量，以及其他子例程局部信息的区域。
# 在大多数情况下，当每个子例程返回的时候，其栈帧将被清除掉，就是说堆栈将会自行实现清理过程。
# 协程(coroutine):处于同等的地位，并可以彼此间进行无缝通信。

def ping_():
    print("PING")
    pong_()

def pong_():
    print("PONG")
    ping_()





import stackless as sl

ping_channel = sl.channel()
pong_channel = sl.channel()

def ping():
    while ping_channel.receive(): #在此阻塞
        print("PING")
        pong_channel.send("from ping")


def pong():
    while pong_channel.receive():
        print("PONG")
        ping_channel.send("from pong")


def coroutine():
    sl.tasklet(ping)()
    sl.tasklet(pong)()

    # 我们需要发送一个消息来初始化这个游戏的状态
    # 否则，两个微进程都会阻塞
    sl.tasklet(ping_channel.send)('startup')

    sl.run()


def main():
    # ping_()     #递归调用recursion导致堆栈溢出
    coroutine()


if __name__ == '__main__':
    main()



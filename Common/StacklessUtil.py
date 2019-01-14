import stackless as sl

import time

# 微进程将排起队来，并不运行，直到调用 stackless.run() 。
# 调度器控制各个微进程运行的顺序，建立一组可以再次被调度的微进程，好让每个都有轮次机会
# 通道使得微进程之间的信息传递成为可能：能够在微进程之间交换信息；能够控制运行的流程。



def tasklet(x):
    print("微进程tasklet：开始"+x)
    time.sleep(1)
    print("微进程tasklet：结束" + x)

def testTasklet():
    sl.tasklet(tasklet)("One")
    sl.tasklet(tasklet)("Two")
    sl.tasklet(tasklet)("Three")
    print("-----------")
    sl.run()

def scheduler(x):
    print("调度器scheduler1："+x)
    sl.schedule()
    print("调度器scheduler2：" + x)
    sl.schedule()
    print("调度器scheduler3：" + x)
    sl.schedule()

def testScheduler():
    sl.tasklet(scheduler)("One")
    sl.tasklet(scheduler)("Two")
    sl.tasklet(scheduler)("Three")
    print("-----------")
    sl.run()




channel = sl.channel()
def receiving_tasklet():
     print("Recieving tasklet started")
     print(channel.receive())
     print("Receiving tasklet finished")

def sending_tasklet():
     print("Sending tasklet started")
     channel.send("send from sending_tasklet")
     print("sending tasklet finished")

def another_tasklet():
     print("Just another tasklet in the scheduler")


def testChannel():
    sl.tasklet(receiving_tasklet)()
    sl.tasklet(sending_tasklet)()
    sl.tasklet(another_tasklet)()
    print("------Recevie Send Another-----")
    sl.run()

    sl.tasklet(sending_tasklet)()
    sl.tasklet(another_tasklet)()
    print("------Send  Another-----")
    sl.run()

    sl.tasklet(another_tasklet)()
    print("------Another-----")
    sl.run()

    print("------Recevie-----")
    sl.tasklet(receiving_tasklet)()
    sl.run()

def main():
    testTasklet()
    # # testScheduler()
    # testChannel()

if __name__ == '__main__':
    main()


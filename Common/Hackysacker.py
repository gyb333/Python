import threading as thread
import random
import sys
import queue


class hackysacker:
    counter = 0
    def __init__(self,name,circle):
        self.name = name
        self.circle = circle
        circle.append(self)
        self.messageQueue = queue.Queue()

        t=thread.Thread(target=self.messageLoop,args=())
        t.start()

    def incrementCounter(self):
        hackysacker.counter += 1
        if hackysacker.counter >= turns:
            while self.circle:
                hs = self.circle.pop()
                if hs is not self:
                    hs.messageQueue.put('exit')
            sys.exit()

    def messageLoop(self):
        while 1:
            message = self.messageQueue.get()
            if message == "exit":
                debugPrint("%s is going home" % self.name)
                sys.exit()
            debugPrint("%s got hackeysack from %s" % (self.name, message.name))
            kickTo = self.circle[random.randint(0,len(self.circle)-1)]
            debugPrint("%s kicking hackeysack to %s" % (self.name, kickTo.name))
            self.incrementCounter()
            kickTo.messageQueue.put(self)

def debugPrint(x):
    if debug:
        print(x)

debug=1
hackysackers=5
turns = 5

def runit(hs=10,ts=10,dbg=1):
    global hackysackers,turns,debug
    hackysackers = hs
    turns = ts
    debug = dbg

    hackysacker.counter= 0
    circle = []
    one = hackysacker('1',circle)

    for i in range(hackysackers):
        hackysacker('i',circle)

    one.messageQueue.put(one)

    try:
        while circle:
            pass
    except:
        #有时我们在清理过程中会遇到诡异的错误。
        pass

if __name__ == "__main__":
    import  datetime as time
    beginTime=time.datetime.now()
    print(time.datetime.strftime(beginTime,'%Y-%m-%d %H:%M:%S'))
    runit(10000,10000,0)
    endTime=time.datetime.now()
    print(time.datetime.strftime(endTime,'%Y-%m-%d %H:%M:%S'))
    seconds=(endTime-beginTime).seconds
    print(seconds)
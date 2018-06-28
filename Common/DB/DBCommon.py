# -*- coding:utf-8 -*-
class DBCommon:
    @classmethod
    def getArgs(cls,procName, *args):
        str = None
        length = len(args)
        if length >= 1:
            str = "select @" + procName
            for i in range(1, length):
                str += ",@_" + procName + "_" + i
        return str
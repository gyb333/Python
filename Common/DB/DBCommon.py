# -*- coding:utf-8 -*-
class DBCommon:
    @classmethod
    def getArgs(cls,procName, args):
        strSQL = "select "
        i=0
        for each in args:
            strSQL += "@_" + procName + "_" + str(i)
            if i<len(args)-1:
                strSQL+=","
            i+=1
        return strSQL
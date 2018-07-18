# -*- coding:utf-8 -*-

import datetime as dt
import pymysql as ps


from Common.DB.DataAccess import DataAccess
from Common.DB.EnumType import  CommandType
from Common.DB.DBCommon import DBCommon

def ExecuteScalar():
    da = DataAccess()
    cmdText = "SELECT now();"
    res = da.ExecuteScalar(cmdText)
    res = da.ExecuteScalarByConn(cmdText)
    print(res)
    print(res['effect_row'])
    print(res['rows'][0])
    cmdText="Truncate table Student;"
    res = da.ExecuteScalar(cmdText)
    res = da.ExecuteScalarByConn(cmdText)
    print(res)

def ExecuteOneOrMany():
    da = DataAccess()
    cmdText = "INSERT INTO Student(name, age,sex) VALUES (%s,%s,%s)"
    args = [('gyb', 10, 1), ('zhansan', 20, 0), ('lisi', 30, 1)]
    rowcount=da.ExecuteMany(cmdText,args)
    rowcount=da.ExecuteScalar(cmdText,('test',11,1))
    rowcount = da.ExecuteScalar(cmdText, ('gyb', 10, 1))

    rowcount = da.ExecuteManyByConn(cmdText, args)
    print(rowcount)
    rowcount = da.ExecuteScalarByConn(cmdText, ('测试', 13, 1))
    print(rowcount)
    rowcount = da.ExecuteScalarByConn(cmdText, ('雇佣兵', 14, 1))
    print(rowcount)

def ExecuteMany():
    da=DataAccess()
    args = [('gyb1', 33, 1), ('张三', 50, 0), ('李四', 70, 1)]
    cmdText=""
    for each in args:
        cmdText+="INSERT INTO Student(name, age,sex) VALUES ('%s',%s,%s);"%each
    rowcount = da.ExecuteScalar(cmdText)
    print(rowcount)

def ExecuteScalarByParams():
    da = DataAccess()
    id =1
    name = 'gyb'
    age = 10
    cmdText="UPDATE Student s set age=age+2 WHERE id=%s AND s.name=%s"
    params=(id,name)
    rowcount=da.ExecuteScalar(cmdText,params)
    rowcount = da.ExecuteScalarByConn(cmdText, params)
    print(rowcount)
    cmdText = "SELECT * FROM Student s WHERE name=%s AND age=%s"
    params = (name, age)
    rowcount = da.ExecuteScalar(cmdText, params)
    rowcount = da.ExecuteScalarByConn(cmdText, params)
    print(rowcount)

def ExecuteNonQueryByParams():
    da = DataAccess()
    name = 'gyb'
    age = 10
    cmdText = "SELECT * FROM Student s WHERE name=%s AND age=%s"
    params = (name, age)
    rowcount = da.ExecuteNonQuery(cmdText, params)
    rowcount = da.ExecuteNonQueryByConn(cmdText, params)
    print(rowcount)


def ExecuteProc():
    da=DataAccess()
    print("--------------------------------------------")
    isFlag=True
    weight=2.2
    amount=3.3
    args=(1,"雇佣兵",isFlag,dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),weight,amount)
    cmdText = "proc_test"
    res= da.ExecuteStoredProcdure(cmdText,args)
    print(res)
    print("--------------------------------------------")
    cmdText = "p1"
    res = da.ExecuteStoredProcdure(cmdText)
    print(res)

def ExecuteProcConn():
    da = DataAccess()
    print("--------------------------------------------")
    cmdText = "p1"
    res = da.ExecuteStoredProcdure(cmdText)
    print(res)

    print("--------------------------------------------")
    isFlag = True
    weight = 2.2
    amount = 3.3
    args = (1, "雇佣兵", isFlag, dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), weight, amount)
    cmdText = "proc_test"
    res = da.ExecuteStoredProcdure(cmdText, args)
    print(res)
    print("--------------------------------------------")
    cmdText = "p1"
    res = da.ExecuteStoredProcdure(cmdText)
    print(res)

def ExecuteStoredProcdureTest(self):
        with self.mysql(None) as cursor:
            try:
                isFlag = True
                weight = 2.2
                amount = 3.3
                params = (1, "雇佣兵", isFlag, '2018-06-29 16:35:15', weight, amount)

                cmdText="p1"
                cursor.callproc(cmdText)
                rs=cursor.fetchall()
                print(rs)

                print("---------------")
                cmdText = "p1"
                cursor.callproc(cmdText)
                cursor.execute("select 1")
                rs = cursor.fetchall()
                print(rs)

                print("---------------")
                cmdText = "proc_test"
                str = DBCommon.getArgs(cmdText, params)
                cursor.callproc(cmdText, args=params)
                cursor.execute(str)
                cursor.execute("select 1")
                rs = cursor.fetchall()
                print(rs)

                cursor.execute("select 1")  # str = DBCommon.getArgs(cmdText, params)
                cursor.execute("select 1")
                params = cursor.fetchall()
                print(params)


                return (rs,params)
            except ps.Error as e:
                print(e)
            finally:
                pass



def main():


    # ExecuteScalar()
    # ExecuteOneOrMany()
    # ExecuteMany()
    # ExecuteScalarByParams()

    # ExecuteNonQueryByParams()
    # ExecuteProc()
    ExecuteProcConn()



if __name__ == '__main__':
        main()
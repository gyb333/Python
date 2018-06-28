# -*- coding:utf-8 -*-
import pymysql as ps

from Common.Config.DBConfig import DBConfig
from Common.DB.EnumType import *
from Common.DB.DBCommon import DBCommon

class DataAccess:
    def __init__(self):
        self.host=DBConfig.getDBHOST()
        self.port = DBConfig.getDBPORT()
        self.user=DBConfig.getDBUSER()
        self.passwd=DBConfig.getDBPASSWORD()
        self.database=DBConfig.getDBName()
        self.charset=DBConfig.getDBCHARSET()
        self.__conn=None
        self.__cursor=None
        self.__dictCursor=None


    @property  # 修饰器
    def Conn(self):
        if self.__conn ==None:
            self.connect2()
        return self.__conn

    @property  # 修饰器
    def Cursor(self):
        if self.__cursor ==None:
            self.__cursor=self.Conn.cursor()
        return self.__cursor

    @property  # 修饰器
    def DictCursor(self):
        if self.__dictCursor == None:
            self.__dictCursor = self.Conn.cursor(cursor=ps.cursors.DictCursor)
        return self.__dictCursor


    def connect(self,host='localhost',port=3306,user='root',passwd='',database='test',charset='utf8'):

        try:
            self.__conn = ps.connect(host=host, user=user, passwd=passwd,db=database, port=port,charset=charset)
        except :
           raise("DataBase connect error,please check the db config.")


    def connect2(self,**kwargs):
        if kwargs=={}:
            self.connect(self.host,self.port,self.user,self.passwd,self.database,self.charset)
        else:
            self.connect(host=kwargs["host"], port=kwargs["port"], user=kwargs["user"], password=kwargs["password"],
            charset=kwargs["charset"], database=kwargs["database"])


    def close(self):
        if not self.__cursor:
            self.__cursor.close()
        if not self.__dictCursor:
            self.__dictCursor.close()
        if not self.__conn:
            self.__conn.close()

    """
        命令类型，如果是sql语句，则为CommandType.Text,否则为   CommandType.StoredProcdure
        返回受影响的行数
        """
    def __Execute(self,cmdText, commandType=CommandType.Text,rowType=RowType.Many,commit=True,*args):
        cursor = None
        count=None
        if commandType == CommandType.StoredProcedure:
            cursor = self.DictCursor
            if args is None:
                cursor.callproc(cmdText)         # cursor.callproc('p2')  # 等价于cursor.execute("call p2()")
            else:
                cursor.callproc(cmdText, args)
                str = DBCommon.getArgs(cmdText, args)
                count=cursor.execute(str)

        else:
            cursor = self.Cursor
            count =cursor.execute(cmdText)
        if rowType== RowType.Many:
            effect_row = cursor.fetchall()
        else:
            effect_row = cursor.fetchone()
        if commit:
            self.Conn.commit()
        return count,effect_row

    def ExecuteNonQuery(self,cmdText, commandType=CommandType.Text,commit=True,*args):
        return  self.__Execute(cmdText,commandType,RowType.Many,commit,args)

    """
    返回查询结果的第一行第一列
    """
    def ExecuteScalar(self,cmdText,commandType=CommandType.Text,commit=True,*args):
        return self.__Execute(cmdText, commandType, RowType.One, commit, args)

    def ExecuteMany(self, cmdText, args, commit=True):
        effect_row = self.Cursor.executemany(cmdText, args)
        lastid =self.Cursor.lastrowid
        if commit:
            self.Conn.commit()
        return effect_row,lastid


    def Execute(self):
        pass


def main():
    da=DataAccess()
    cmdText="SELECT now();"
    res=da.ExecuteScalar(cmdText)
    print(res[1][0])
    print(type(res[1][0]))

    cmdText="INSERT INTO Student(name, age,sex) VALUES (%s,%s,%s)"
    args=[('gyb',10,1),('zhansan',20,0),('lisi',30,1)]
    rowcount=da.ExecuteMany(cmdText,args)


    print(rowcount)

if __name__ == '__main__':
        main()
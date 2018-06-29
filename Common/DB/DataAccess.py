# -*- coding:utf-8 -*-
import pymysql as ps
import contextlib


from Common.Config.DBConfig import DBConfig
from Common.DB.EnumType import *
from Common.DB.DBCommon import DBCommon

class DataAccess:
    def __init__(self,config=True):
        if config:
            self.host=DBConfig.getDBHOST()
            self.port = DBConfig.getDBPORT()
            self.user=DBConfig.getDBUSER()
            self.passwd=DBConfig.getDBPASSWORD()
            self.database=DBConfig.getDBName()
            self.charset=DBConfig.getDBCHARSET()
        self.__conn=None
        self.__cursor=None
        self.__dictCursor=None

    def __del__(self):
        self.close()


    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__dictCursor:
            self.__dictCursor.close()
        if self.__conn:
            self.__conn.close()

    @property  # 修饰器
    def Conn(self):
        if self.__conn ==None:
            self.__conn=self.connect2()
        return self.__conn

    @property  # 修饰器
    def Cursor(self):
        if self.__cursor ==None:
            self.__cursor=self.Conn.cursor()
        return self.__cursor

    @Cursor.setter
    def Cursor(self, value):
        self.__cursor = value

    @property  # 修饰器
    def DictCursor(self):
        if self.__dictCursor == None:
            self.__dictCursor = self.Conn.cursor(cursor=ps.cursors.DictCursor)
        return self.__dictCursor


    def connect(self,host='localhost',port=3306,user='root',passwd='',database='test',charset='utf8'):
        try:
            conn = ps.connect(host=host, user=user, passwd=passwd,db=database, port=port,charset=charset)
            return conn
        except :
           raise("DataBase connect error,please check the db config.")


    def connect2(self,**kwargs):
        conn=None
        if kwargs=={}:
            conn=self.connect(self.host,self.port,self.user,self.passwd,self.database,self.charset)
        else:
            conn=self.connect(host=kwargs["host"], port=kwargs["port"], user=kwargs["user"], password=kwargs["password"],
            charset=kwargs["charset"], database=kwargs["database"])
        return  conn



    """
        命令类型，如果是sql语句，则为CommandType.Text,否则为   CommandType.StoredProcdure
        返回受影响的行数
        """
    def __Execute(self,cmdText, params=None,rowType=RowType.Many,commit=True,cursor=None):
        count=None
        try:
            if not cursor:
                cursor=self.Cursor
            if params is None:
                effect_row =cursor.execute(cmdText)
            else:
                effect_row = cursor.execute(cmdText,params)

            if rowType== RowType.Many:
                rows = cursor.fetchall()
            else:
                rows = cursor.fetchone()
            return { 'effect_row': effect_row,'rows': rows}
        except ps.Error as e:
            print(e)
        finally:
            if commit:
                self.Conn.commit()








    def ExecuteNonQuery(self,cmdText,params=None,commit=True):
        return  self.__Execute(cmdText,params,RowType.Many,commit)

    """
    返回查询结果的第一行第一列
    """
    def ExecuteScalar(self,cmdText,params=None,commit=True):
        return self.__Execute(cmdText,params,  RowType.One, commit)

    def ExecuteMany(self, cmdText,params=None, commit=True):
        try:
            effect_row = self.Cursor.executemany(cmdText, params)
            lastid =self.Cursor.lastrowid
            return {'effect_row': effect_row, 'lastid': lastid}
        finally:
            if commit:
                self.Conn.commit()




    # 定义上下文管理器，连接后自动关闭连接
    @contextlib.contextmanager
    def mysql(self,conn=None):
        close =False
        if not conn:
            close=True
            conn=self.connect2()
        if type(conn)==ps.connections.Connection:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                conn.commit()
                cursor.close()
                if close:
                    conn.close()



    def ExecuteNonQueryByConn(self,cmdText,params=None,conn=None):
        with self.mysql(conn) as cursor:
            return self.__Execute(cmdText,params,RowType.Many,False,cursor)

    def ExecuteScalarByConn(self,cmdText,params=None,conn=None):
        with self.mysql(conn) as cursor:
            return self.__Execute(cmdText,params, RowType.One,False, cursor)

    def ExecuteManyByConn(self, cmdText,params=None,conn=None):
        with self.mysql(conn) as cursor:
            try:
                effect_row = cursor.executemany(cmdText, params)
                lastid = cursor.lastrowid
                return {'effect_row': effect_row, 'lastid': lastid}
            except ps.Error as e:
                print(e)
            finally:
                pass


    def ExecuteStoredProcdure(self, cmdText, params=None,conn=None):
        with self.mysql(conn) as cursor:
            try:
                if not params:
                    cursor.callproc(cmdText)
                    rs=cursor.fetchall()
                else:
                    str = DBCommon.getArgs(cmdText, params)
                    cursor.callproc(cmdText, args=params)
                    rs = cursor.fetchall()
                    cursor.execute(str)  # str = DBCommon.getArgs(cmdText, params)
                    cursor.execute("select 1")
                    params = cursor.fetchall()
                return (rs,params)
            except ps.Error as e:
                print(e)
            finally:
                pass







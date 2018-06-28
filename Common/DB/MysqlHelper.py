# -*- coding:utf-8 -*-
import logging
import pymysql as ps
from functools import  singledispatch

from Config.DBConfig import DBConfig

#logger = logging.getLogger(__name__)

class MysqlHelper:





    def cud(self,sql,params):
        self.open()
        try:
            self.curs.execute(sql,params)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.close()

    def find(self,sql,params):
        self.open()
        try:
            result=self.curs.execute(sql,params)
            self.close()
            return  result
        except:
            pass







def main():
    dbHelper=MysqlHelper()
    dbHelper.connect2()

if __name__ == '__main__':
        main()
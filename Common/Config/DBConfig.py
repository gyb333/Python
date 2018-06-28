from Common.Config.ConfigHelper import ConfigHelper

class DBConfig:
    __Section="DB"
    __ConfigFileName="DBConfig.ini"
    config = ConfigHelper(__ConfigFileName)
    __DBName = config.getValue(__Section, "DB_NAME")
    __DBHOST = config.getValue(__Section, "DB_HOST")
    __DBPORT = int(config.getValue(__Section, "DB_PORT"))
    __DBUSER = config.getValue(__Section, "DB_USER")
    __DBPASSWORD = config.getValue(__Section, "DB_PASSWORD")
    __DBCHARSET = config.getValue(__Section, "DB_CHARSET")
    __LOGPATH = config.getValue(__Section, "LOG_PATH")

    __slots__ = ()  # 定义__slots__   限制对象实例不能添加属性

    @classmethod
    def getDBName(cls):
        return cls.__DBName
    @classmethod
    def getDBHOST(cls):
        return cls.__DBHOST

    @classmethod
    def getDBPORT(cls):
        return cls.__DBPORT

    @classmethod
    def getDBUSER(cls):
        return cls.__DBUSER

    @classmethod
    def getDBPASSWORD(cls):
        return cls.__DBPASSWORD

    @classmethod
    def getDBCHARSET(cls):
        return cls.__DBCHARSET

    @classmethod
    def getLOGPATH(cls):
        return cls.__LOGPATH

def main():
    DBConfig.Test="test"
    print(DBConfig.getDBHOST())

    DBConfig.config.setValue("key","value","DB")
    DBConfig.config.setValue("test", "ceshi", "DB")
    DBConfig.config.save("w+")



if __name__ == '__main__':
        main()





import os
from Common.Config.ConfigManager import Config

class ConfigHelper:
    __slots__ = ("__cur_path","__config_path","__conf")     # 定义__slots__

    def __init__(self,configName):
        self.__getConfig(configName)

    def __getConfig(self,configName):
        # 获取文件的当前路径（绝对路径）
        self.__cur_path = os.path.dirname(os.path.realpath(__file__))
        # 获取config.ini的路径
        self.__config_path = os.path.join(self.__cur_path, configName)
        self.__conf = Config()
        try:
            self.__conf.read(self.__config_path)
        except:
            raise(configName +" read  error please check the file path ")

    @property  # 修饰器
    def configParser(self):
        return self.__conf

    @configParser.setter
    def configParser(self, value):
        self.__conf = value


    def getValue(self,section,key):
        return self.__conf.get(section,key)

    def addSection(self,section='config'):
        self.__conf.add_section(section)

    def setValue(self,key,value,section='config'):
        self.__conf.set(section,key,value)

    def save(self,mode='a'):
        with open(self.__config_path,mode=mode,encoding='utf-8') as fw:
            self.__conf.write(fw)


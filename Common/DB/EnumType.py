
# -*- coding:utf-8 -*-
from enum import Enum


class CommandType(Enum):
    Text = 1    #文本命令。（默认。）
    StoredProcedure = 4 #存储过程的名称
    TableDirect = 512   #表的名称

class RowType(Enum):
    One=1
    Many=2
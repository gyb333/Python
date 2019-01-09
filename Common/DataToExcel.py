# coding:utf-8

import xlrd
import xlwt
# workbook相关
from openpyxl.workbook import Workbook
# ExcelWriter，封装了很强大的excel写的功能
from openpyxl.writer.excel import ExcelWriter
# 一个eggache的数字转为列字母的方法
from openpyxl.utils import get_column_letter
from openpyxl.reader.excel import load_workbook


def write_to_excel_with_openpyxl(df, columnHeaders, filepath="save.xlsx"):
  # 设置文件输出路径与名称
  # 新建一个workbook
  wb = Workbook()
  from zipfile import ZipFile, ZIP_DEFLATED
  archive = ZipFile(filepath, 'w', ZIP_DEFLATED)
  # 新建一个excelWriter
  ew = ExcelWriter(workbook=wb,archive=archive)

  # 第一个sheet是ws
  ws = wb.worksheets[0]
  # 设置ws的名称
  ws.title = "range names"
  length=len(columnHeaders)
  # 写第一行，标题行
  for i in range(1, length+ 1):
   value=columnHeaders[i - 1]
   ws.cell(1,i,value)

  # 写第二行及其以后的那些行
  i = 2
  for index, row in df.iterrows():
      for j in range(1, length + 1):
          ws.cell(i,j,row[j-1])
      i += 1
  # 写文件
  ew.save()




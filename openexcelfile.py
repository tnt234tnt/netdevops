# coding: utf-8
#打开EXCEL文件并赋值变量
#############################
#import modles
import xlrd
import xlwt
import xlutils
##############################
#Code

def openexcelfile(self):
    book = xlrd.open_workbook(self)
    sheet = book.sheet_by_index(0)
    

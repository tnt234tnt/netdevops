# coding: utf-8
#用于打开当前表格并获取除第一行外的所有数据
for i in range(num):
    if i != 0:
        row = sheet.row_values(i)
        print(str.strip(row[0]),row[1],row[2],row[3])
        

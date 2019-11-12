#!/usr/bin/env python3
# -*- coding: UTF-8 –*-
#用于集合各模块，进行F5配置的自动化脚本，思路为使用源EXCEL文件，通过固定格式的EXCEL文件，进行POOL/MEMBER/VS的自动化创建。
from classfile import class_f5
from classfile import class_excel
import os
#生成一个菜单，用户通过菜单进行交互。 
#打开F5的EXCEL表格文件，并获取相应的内容。
#判断文件是否存在，如果不存在，则不执行程序！
class F5Operation():
    def __init__(self):
        f5filename = input(">>>请输入EXCEL文件的名称（无需输入文件后缀名）:")
        if os.path.exists('file//' + f5filename + '.xlsx') == False:
            print('>>>你输入的文件名：' + f5filename + '.xlsx,不存在！！！')
        else:
            f5file = excel(('file/'+ f5filename + '.xlsx'),0)
            rowcol =f5file.getRowsColsNum()
 
#开始循环表格的行数，进行配置POOL,MEMBER,VS。
            for i in range(rowcol[0]):
#忽略第一行表头。 
                if i != 0 :
#获取第一行表格的值。
                    f5row = f5file.getRowValues(i)
#对表格中的相关内容进行赋值，并删除空格。
                    deviceip = f5row[1].strip()
                    username = f5row[2].strip()
                    password = f5row[3].strip()
                    poolname = f5row[4].strip()
                    poolmonitor = f5row[5].strip()
                    pooldesc = f5row[6].strip()
                    member = f5row[7].strip()
                    memberlist = member.split(',')
                    vsname = f5row[8].strip()
                    vsdesc = f5row[9].strip()
                    vsip = f5row[10].strip()
                    protocol = f5row[11].strip()
                    persist = f5row[12].strip()
                    vsprofile = f5row[13].strip()
                    snattype = f5row[14].strip()
                    snatpoolname = f5row[15].strip()
#如果表格的内容为空，就将该值赋值为NONE。
                    if persist == '':
                        persist = None
                    if vsprofile == '':
                        vsprofile = None
                    if snattype == '':
                        snattype = None
                    if snatpoolname == '':
                        snatpoolname =None
                    sourceAddressTranslation = {'pool':snatpoolname,'type':snattype}
#如果是第一行时，执行第一次连接。
                    if i == 1:
                        f5ltm = class_f5.F5LTMClass(deviceip,username,password) #连接设备
                        f5ltm.createPool(poolname,poolmonitor,pooldesc)  #新建POOL
                        for index in range(len(memberlist)): #获得MEMBER的数量
                            memname = memberlist[index]
                            f5ltm.createMember(poolname,memname) #新建MEMBER
                        f5ltm.createVs(vsname,vsdesc,poolname,vsip,protocol,persist=persist,profiles= vsprofile,
                                       sourceAddressTranslation=sourceAddressTranslation) #新建VS。
#如果表格第二行以后还是第一次连接的设备，就不在次进行连接，而是直接进行配置。
                    elif f5ltm.mgmt.hostname == deviceip:
                        f5ltm.createPool(poolname,poolmonitor,pooldesc) 
                        for index in range(len(memberlist)):
                            memname = memberlist[index]
                            f5ltm.createMember(poolname,memname)
                        f5ltm.createVs(vsname,vsdesc,poolname,vsip,protocol,persist=persist,profiles= vsprofile,
                                       sourceAddressTranslation=sourceAddressTranslation)
                    else:
#直到表格中的帐号密码已经是其他设备，那就重新进行一次连接。
                        f5ltm = class_f5.F5LTMClass(deviceip,username,password)
                        f5ltm.createPool(poolname,poolmonitor,pooldesc)
                        for index in range(len(memberlist)):
                            memname = memberlist[index]
                            f5ltm.createMember(poolname,memname)
                        f5ltm.createVs(vsname,vsdesc,poolname,vsip,protocol,persist=persist,profiles= vsprofile,
                                        sourceAddressTranslation=sourceAddressTranslation)
                else:
                    pass

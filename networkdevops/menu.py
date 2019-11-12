#!/usr/bin/env python3
# -*- coding: UTF-8 –*-
from classfile import class_f5operation
from classfile import class_f5syncoperation
from classfile import class_f5query
import os
#创建一个菜单，用于调用需要操作的设备清单
#1、F5设备的POOL/MEMBER/VS自动创建。
#2、在第一项的基础上，使用同一个文件，进行设备的同步。
#3、查询设备上的基本信息，如POOL清单，MEMBER清单，VS清单等信息。
while 1==1:
    str1 = '*' * 60
    print("\n"+str1)
    print(">>>1、F5设备配置自动化(VS、POOL、MEMBER)！！！")
    print(">>>2、F5设备配置同步（目标设备需为双机）！！！")
    print(">>>3、F5设备信息查询！！！")
    print(">>>4、退出程序！！！")
    print(str1 + "\n\n")
    menu = input(">>>请选择相关操作,输入菜单对应的数字："+ "\n")

    if menu == "1":
        run = class_f5operation.F5Operation()
    elif menu == "2":
        run = class_f5syncoperation.F5Sync()
    elif menu == "3":
        print(str1)
        print(">>>1、查询VS信息！！！")
        print(">>>2、查询POOL及MEMBER信息！！！")
        print(">>>3、查询Monitor信息！！！")
        print(str1)
        menuindex = input(">>>请选择相关操作,输入菜单对应的数字：" + "\n")
        if menuindex == "1":
            run = class_f5query.F5query()
            if run.rowcol == []:
                continue
            else:
                run.queryAllVs()
        elif menuindex == "2":
            run = class_f5query.F5query()
            if run.rowcol == []:
                continue
            else:
                run.queryAllPool()
        elif menuindex == "3":
            print(">>>1、查询TCP Monitor信息！！！")
            print(">>>2、查询Http Monitor信息！！！")
            print(">>>3、查询Https Monitor信息！！！")
            monitorindex = input(">>>请选择相关操作,输入菜单对应的数字：" + "\n")
            if monitorindex == "1":
                run = class_f5query.F5query()
                if run.rowcol == []:
                    continue
                else:
                    run.queryAllMonitor("tcp")
            elif monitorindex == "2":
                run = class_f5query.F5query()
                if run.rowcol == []:
                    continue
                else:
                    run.queryAllMonitor("http")
            elif monitorindex == "3":
                run = class_f5query.F5query()
                if run.rowcol == []:
                    continue
                else:
                    run.queryAllMonitor("https")
            else:
                print(">>>输入错误，请重新输入！！！")
                continue
        else:
            print(">>>输入错误，请重新输入！！！")
            continue
    elif menu == "4":
        print(">>>程序退出！！！")
        break
    else:
        print(">>>输入错误，请重新输入！！！")
        continue

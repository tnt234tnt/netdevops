from classfile import class_f5
from classfile import class_excel
import os
#菜单三三，对F5Operation中操作的设备查询相关信息。
class F5query():
    def __init__(self):
        f5filename = input(">>>请输入EXCEL文件的名称（无需输入文件后缀名）:")
        if os.path.exists('file//' + f5filename + '.xlsx') == False:
            print('>>>你输入的文件名：' + f5filename + '.xlsx,不存在！！！')
            rowcol = []
            self.rowcol = rowcol
        else:
            f5file = class_excel.excel(('file/'+ f5filename + '.xlsx'),0)
            rowcol =f5file.getRowsColsNum()
            self.rowcol = rowcol
            self.f5file = f5file

    def queryAllPool(self):
        for i in range(self.rowcol[0]):
            if i != 0 :
                f5row = self.f5file.getRowValues(i)
                deviceip = f5row[1].strip()
                username = f5row[2].strip()
                password = f5row[3].strip()
                if i ==1:
                    query = class_f5.F5LTMClass(deviceip,username,password)
                    poollist = query.getAllPoolName()
                    print("\n\n>>>设备：" + query.mgmt.hostname + "共有" + str(len(poollist)) +"个POOL！！！" )
                    for index in range(len(poollist)):
                        poolname = poollist[index]
                        member = query.getPoolAllMemberName(poolname)
                        print(">>>POOL:" + poolname + ",包含的Member对象为：" + str(member))

                elif  query.mgmt.hostname == deviceip:
                    pass
                else:
                    print("\n")
                    query = class_f5.F5LTMClass(deviceip,username,password)
                    poollist = query.getAllPoolName()
                    print("\n\n>>>设备：" + query.mgmt.hostname + "共有" + str(len(poollist)) +"个POOL！！！" )
                    for index in range(len(poollist)):
                        poolname = poollist[index]
                        member = query.getPoolAllMemberName(poolname)
                        print(">>>POOL:" + poolname + ",包含的Member对象为：" + str(member))

    def queryAllVs(self):
        for i in range(self.rowcol[0]):
            if i != 0 :
                f5row = self.f5file.getRowValues(i)
                deviceip = f5row[1].strip()
                username = f5row[2].strip()
                password = f5row[3].strip()
                if i ==1:
                    query = class_f5.F5LTMClass(deviceip,username,password)
                    vslist = query.getAllVsName()
                    print("\n\n>>>设备：" + query.mgmt.hostname + "共有" + str(len(vslist)) +"个VS！！！" )
                    print(">>>设备包含的VS有：" + str(vslist) + "！！！")

                elif  query.mgmt.hostname == deviceip:
                    pass
                else:
                    print("\n")
                    query = class_f5.F5LTMClass(deviceip,username,password)
                    vslist = query.getAllVsName()
                    print("\n\n>>>设备：" + query.mgmt.hostname + "共有" + str(len(vslist)) +"个vs！！！" )
                    print(">>>设备包含的VS有：" + str(vslist) + "！！！")
    def queryAllMonitor(self,monitortype):
        for i in range(self.rowcol[0]):
            if i != 0 :
                f5row = self.f5file.getRowValues(i)
                deviceip = f5row[1].strip()
                username = f5row[2].strip()
                password = f5row[3].strip()
                if i ==1:
                    query = class_f5.F5MONITORClass(deviceip,username,password)
                    monitoralllist = query.getAllMonitor()
                    monitorlist = query.getMonitor(monitortype)
                    print("\n\n>>>设备：" + query.mgmt.hostname + "共有" + str(len(monitorlist)) +"个Monitor！！！" )
                    print(">>>设备Monitor类型为" + monitortype  + "的对象有："+ str(monitorlist) + "！！！")

                elif  query.mgmt.hostname == deviceip:
                    pass
                else:
                    print("\n")
                    query = class_f5.F5MONITORClass(deviceip,username,password)
                    monitoralllist = query.getAllMonitor()
                    monitorlist = query.getMonitor(monitortype)
                    print("\n\n>>>设备：" + query.mgmt.hostname + "共有" + str(len(monitorlist)) +"个Monitor！！！" )
                    print(">>>设备Monitor类型为" + monitortype  + "的对象有："+ str(monitorlist) + "！！！")
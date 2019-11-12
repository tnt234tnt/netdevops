from classfile import class_f5
from classfile import class_excel
import os
#菜单二，对F5Operation中操作的设备进行双机同步配置。
class F5Sync():
    def __init__(self):
        f5filename = input(">>>请输入EXCEL文件的名称（无需输入文件后缀名）:")
        if os.path.exists('file//' + f5filename + '.xlsx') == False:
            print('>>>你输入的文件名：' + f5filename + '.xlsx,不存在！！！')
        else:
            f5file = class_excel.excel(('file/'+ f5filename + '.xlsx'),0)
            rowcol =f5file.getRowsColsNum()

            for i in range(rowcol[0]):
                if i != 0 :
                    f5row = f5file.getRowValues(i)
                    deviceip = f5row[1].strip()
                    username = f5row[2].strip()
                    password = f5row[3].strip()
                    if i ==1:
                        sync = class_f5.F5CMSYNCClass(deviceip,username,password)
                        synclist = sync.getDeviceName()
                        print(">>>设备" + deviceip + "上的同步组有："+ str(synclist))
                        groupname = input(">>>请输入需要同步的同步组名称：")
                        if groupname in synclist:
                            sync.syncDeviceToGroup(groupname)
                        else:
                            print(">>>输入有误" + groupname + "不在设备" + deviceip + "同步组中，请检查！！！")
                    elif  sync.mgmt.hostname == deviceip:
                        pass
                    else:
                        sync = class_f5.F5CMSYNCClass(deviceip,username,password)
                        synclist = sync.getDeviceName()
                        print(">>>设备"  + deviceip + "上的同步组有："+ str(synclist))
                        groupname = input(">>>请输入需要同步的同步组名称：")
                        if groupname in synclist:
                            sync.syncDeviceToGroup(groupname)
                        else:
                            print(">>>输入有误" + groupname + "不在设备" + deviceip + "同步组中，请检查！！！")
                    
    
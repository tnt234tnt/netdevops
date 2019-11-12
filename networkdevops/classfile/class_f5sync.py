#!/usr/bin/env python3
# -*- coding: UTF-8 –*-
#F5,CM类，用于同步双机配置。
import f5.bigip
from f5.bigip import ManagementRoot
import class_f5conn
from class_f5conn import F5CONNClass

class F5CMSYNCClass(F5CONNClass):
#链接F5设备，并对函数进行赋值；Deviceip为设备IP地址，Username为设备用户名，Password为设备密码。默认端口号为：443.
    def __init__(self,deviceip,username,password):
        F5CONNClass.__init__(self,deviceip,username,password)
        self.device_groups = self.mgmt.tm.cm.device_groups
        self.device_group = self.mgmt.tm.cm.device_groups.device_group
        
#获取设备同步组的名称列表。
    def getDeviceName(self):
        device_collection = self.device_groups.get_collection()
        devicelist = []
        for device in device_collection:
            devicelist.append(device.name)
        self.devicelist = devicelist
        return self.devicelist
    
#配置由设备同步到组。同步名称为同步组的名称，就是设备WEB界面下，
#设备管理下的DEVICE GROUPS下自定义的名称，不是单个设备的名称，设备同步组的列
#表可以通过getDeviceName()函数获得。通过与自己的设备对应即可。下列函数DEVICENAME的名称即为
    def syncDeviceToGroup(self,devicename):
        if self.device_group.exists(name = devicename) == True:
            devicesync = self.device_group.load(name = devicename)
            devicesync.sync_to()
            print(">>>同步设备配置到同步组成功！！！")
        else:
            print(">>>同步组名称：" + devicename + "不存在，请检查配置文件！！！")   

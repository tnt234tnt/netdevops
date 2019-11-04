#用于连接F5设备的类，父类。
import f5.bigip
from f5.bigip import ManagementRoot

class F5CONNClass():
#链接F5设备，并对函数进行赋值；Deviceip为设备IP地址，Username为设备用户名，Password为设备密码。默认端口号为：443.
    def __init__(self,deviceip,username,password):
        mgmt = f5.bigip.ManagementRoot(deviceip,username,password)
        self.mgmt = mgmt
        print(">>>设备连接成功，连接的设备是" + deviceip + ",用户名为" + username + "！！！")
        print(">>>设备软件版本为:" + mgmt.tmos_version + "！！！")

#!/usr/bin/env python3
# -*- coding: UTF-8 –*-
import f5.bigip
from f5.bigip import ManagementRoot

#用于连接F5设备的类，父类。
class F5CONNClass():
#链接F5设备，并对函数进行赋值；Deviceip为设备IP地址，Username为设备用户名，Password为设备密码。默认端口号为：443.
    def __init__(self,deviceip,username,password):
        mgmt = f5.bigip.ManagementRoot(deviceip,username,password)
        self.mgmt = mgmt
        print("<<<设备连接成功，连接的设备是" + deviceip + ",用户名为" + username + ">>>")
        print("<<<设备软件版本为:" + mgmt.tmos_version + ">>>")


# F5-LTM类，用于新建POOL,Member,VS。
class F5LTMClass(F5CONNClass):
    # 链接F5设备，并对函数进行赋值；Deviceip为设备IP地址，Username为设备用户名，Password为设备密码。默认端口号为：443.
    def __init__(self, deviceip, username, password):
        F5CONNClass.__init__(self, deviceip, username, password)

    # 设备连接成功后，开始创建POOL和MEMBER。参数为POOL的名称，健康检查类型，描述。
    def createPool(self, poolname, monitor, description):
        poolinfo = self.mgmt.tm.ltm.pools.pool
        # 判断传入的POOL名称在设备中是否存在，如果存在，则不进行创建新的POOL。
        if poolinfo.exists(name=poolname) == True:
            print(">>>Pool：" + poolname + "的名称已经存在，请检查后修改！！！")
        else:
            pool = self.mgmt.tm.ltm.pools.pool.create(name=poolname, monitor=monitor, description=description,
                                                      partition='Common')
            pools = self.mgmt.tm.ltm.pools.pool.load(partition='Common', name=poolname)
            self.pools = pools
            print(">>>pool:" + poolname + "创建成功！！！")
        return

    # 新建好POOL后，在新建的POOL的基础上新增POOL的MEMBER。POOLNAME表示在那个POOL新建MEMBER。membername的格式为IP:PORT，示例：192.168.1.5:80。
    def createMember(self, poolname, membername):
        poolinfo = self.getAllPoolName()
        if (poolname in poolinfo) == False:
            print(">>>POOL：" + poolname + "不存在,请检查配置文件！！！")
        else:
            memberinfo = self.getPoolAllMemberName(poolname)
            pools = self.mgmt.tm.ltm.pools.pool.load(partition='Common', name=poolname)
            if (membername in memberinfo) == False:
                members = pools.members_s.members.create(partition='Common', name=membername)
                print(">>>" + poolname + "的Member:" + membername + "创建成功！！！")
            else:
                print(">>>" + poolname + "Member:" + membername + "已经存在！！！")

    # 新建VS。参数有NAME:VS的名称，description：VS的描述，pool：要关联的POOL；
    # destination：VS监听地址，格式为IP:PORT，ipProtocol，VS的IP协议，TCP或UDP；
    # persist为会话保持方式，根据业务类型，如果业务为HTTP业务，会话保持一般为COOKIE，如果业务类型为TCP，会话保持就为TCP或目标地址或源地址保持。
    # profiles参数为PROFILE的参数。
    # profiles = 'fasthttp'时，TYPE为 Performance(HTTP),此时会话保持只能是persist= 'cookie'。
    # profiles = 'tcp'时，TYPE为 Standard,此时会话保持不能是persist= 'cookie'。
    # profiles = 'fastL4'时，TYPE为 Forwarding,此时会话保持不能是persist= 'cookie'。
    # '示例：f5ltm.createVs("vspportt7","test vs",'poolsoor','10.99.100.127:80','tcp',persist='cookie',profiles= 'fasthttp',sourceAddressTranslation = {'pool' :"snat_pool",'type':"snat" })'
    properties = {'persist': None, 'profiles': None, 'sourceAddressTranslation': {}}

    def createVs(self, vsname, description, poolname, destinationip, protocol, **properties):
        vsinfo = self.mgmt.tm.ltm.virtuals.virtual
        if vsinfo.exists(name=vsname) == True:
            print(">>>VS：" + vsname + "已经存在！！！")
        else:
            vs = self.mgmt.tm.ltm.virtuals.virtual.create(name=vsname,
                                                          partition='Common',
                                                          description=description,
                                                          pool=poolname,
                                                          destination=destinationip,
                                                          ipProtocol=protocol,
                                                          mask='255.255.255.255',
                                                          **properties)
            vss = self.mgmt.tm.ltm.virtuals.virtual.load(name=vsname)
            self.vss = vss
            print(">>>VS:" + vsname + "创建成功！！！")
            return

        # 获取所有的POOL名称信息。返回POOL列表。

    def getAllPoolName(self):
        poollist = []
        pool_collection = self.mgmt.tm.ltm.pools.get_collection()
        for pool in pool_collection:
            poollist.append(pool.name)
        self.poollist = poollist
        return self.poollist

    # 获取所有的VS名称信息。返回VS列表。
    def getAllVsName(self):
        vslist = []
        vs_collection = self.mgmt.tm.ltm.virtuals.get_collection()
        for vs in vs_collection:
            vslist.append(vs.name)
        self.vslist = vslist
        return self.vslist

    # 获取指定POOL下所有MEMBER成员信息。返回MEMBER列表。参数为设备上存在的一个POOL名称。
    def getPoolAllMemberName(self, poolname):
        poolinfo = self.getAllPoolName()
        memberlist = []
        if (poolname in poolinfo) == False:
            print(">>>该POOL：" + poolname + "不存在,请检查配置文件！！！")
        else:
            pool = self.mgmt.tm.ltm.pools.pool.load(partition='Common', name=poolname)
            members_collection = pool.members_s.get_collection()
            for member in members_collection:
                memberlist.append(member.name)
        if memberlist == []:
            self.memberlist = memberlist
            return self.memberlist
        else:
            self.memberlist = memberlist
            return self.memberlist

    # 修改VS状态。参数为VS的名称和希望改变的状态，ENABLE为开启，DISABLE为关闭。
    def modfiyVsStatus(self, vsname, status):
        vsinfo = self.getAllVsName()
        if (vsname in vsinfo) == False:
            print(">>>该VS：" + vsname + "不存在,请检查配置文件！")
        else:
            vsinfo = self.mgmt.tm.ltm.virtuals.virtual.load(partition='Common', name=vsname)
            if status == "enable":
                vsinfo.modify(enabled='Ture')
                vsinfo.update
                print(">>>VS:" + vsname + "启用成功！！！")
            elif status == "disable":
                vsinfo.modify(disabled='Ture')
                vsinfo.update
                print(">>>VS:" + vsname + "禁用成功！！！")
            else:
                print(">>>第二个参数错误，请重新输入，参数为enable或disable!!!!")

    # 修改MEMBER状态。输入的参数为POOL的名称和MEMBER的名称和希望改变的状态。
    def modfiyMemberStatus(self, poolname, membername, status):
        poolinfo = self.getAllPoolName()
        if (poolname in poolinfo) == False:
            print(">>>POOL：" + poolname + "不存在,请检查配置文件！")
        else:
            memberinfo = self.getPoolAllMemberName(poolname)
            if memberinfo != []:
                if (membername in memberinfo) == False:
                    print(">>>Member：" + membername + "不存在,请检查配置文件")
                else:
                    pool = self.mgmt.tm.ltm.pools.pool.load(name=poolname)
                    member = pool.members_s.members.load(partition='Common', name=membername)
                    if status == "enable":
                        member.modify(session='user-enabled')
                        member.update
                        print(">>>" + membername + "已经启用，状态为：" + member.session + "！！！")
                    elif status == "disable":
                        member.modify(session='user-disabled')
                        member.update
                        print(">>>" + membername + "已经禁用，状态为：" + member.session + "！！！")
                    else:
                        print(">>>控制参数错误，请重新输入，参数为enable或disable！！！")
            else:
                return


# 该函数用于新建MONITOR，查看MONITOR状态等。
# 定义Monitor类，继承父类f5ltmclass，
class F5MONITORClass(F5CONNClass):
    # 初始化函数

    def __init__(self, deviceip, username, password):
        F5CONNClass.__init__(self, deviceip, username, password)
        self.http = self.mgmt.tm.ltm.monitor.https.http
        self.https = self.mgmt.tm.ltm.monitor.https_s.https
        self.tcp = self.mgmt.tm.ltm.monitor.tcps.tcp
        self.monitor = self.mgmt.tm.ltm.monitor

    # 新建MONITOR，类型为三类，TCP,HTTP,HTTPS，其他的利用率不高，就不做了。
    # 输入的参数有5个，monitortype为要新建的Monitor类型，TCP/HTTP/HTTPS，monitorname为要新建的monitor名称，send为要发送的消息，recv为返回的消息，recvDisable为失败返回的消息，一般用不到！
    recvmsg = {'recvDisable': None}

    def createMonitor(self, monitortype, monitorname, send, recv, **recvmsg):
        http = self.http
        https = self.https
        tcp = self.tcp
        # 首先检查输入的监控类型，根据类型添加相应的MONITOR。
        if monitortype == 'tcp':
            if tcp.exists(name=monitorname) == True:
                print(">>>TcpMonito" + monitorname + "已经存在，请检查配置文件！！！")
            else:
                tcpmonitor = tcp.create(name=monitorname, send=send, recv=recv, **recvmsg)
                print(">>>TcpMonito" + monitorname + "创建成功！！！")
        elif monitortype == 'http':
            if http.exists(name=monitorname) == True:
                print(">>>HttpMonito" + monitorname + "已经存在，请检查配置文件！！！")
            else:
                httpmonitor = http.create(name=monitorname, send=send, recv=recv, **recvmsg)
                print(">>>HttpMonito" + monitorname + "创建成功！！！")
        elif monitortype == 'https':
            if https.exists(name=monitorname) == True:
                print(">>>HttpsMonito" + monitorname + "已经存在，请检查配置文件！！！")
            else:
                httpsmonitor = https.create(name=monitorname, send=send, recv=recv, **recvmsg)
                print(">>>HttpsMonito" + monitorname + "创建成功！！！")
        else:
            print(">>>您输入的Monitor类型不正确，支持的类型有TCP,HTTP,HTTPS,请输入前3种类型的Monitor类型！！！")

    # 获取所有MONITOR的名字。包含TCP/HTTP/HTTPS。
    def getAllMonitor(self):
        monitorhttplist = []
        monitorhttpslist = []
        monitortcplist = []
        monitor_http_collection = self.monitor.https.get_collection()
        monitor_https_collection = self.monitor.https_s.get_collection()
        monitor_tcp_collection = self.monitor.tcps.get_collection()
        [monitorhttplist.append(monitorhttp.name) for monitorhttp in monitor_http_collection]
        [monitorhttpslist.append(monitorhttps.name) for monitorhttps in monitor_https_collection]
        [monitortcplist.append(monitortcp.name) for monitortcp in monitor_tcp_collection]
        self.monitorhttplist = monitorhttplist
        self.monitorhttpslist = monitorhttpslist
        self.monitortcplist = monitortcplist
        return self.monitorhttplist, self.monitorhttpslist, self.monitortcplist

    # 分别获取指定类型的Monitor列表。参数为TCP/HTTP/HTTPS，仅支持3种。
    def getMonitor(self, monitortype):
        if monitortype == 'tcp':
            return self.monitortcplist
        elif monitortype == 'http':
            return self.monitorhttplist
        elif monitortype == 'https':
            return self.monitorhttpslist
        else:
            print(">>>您输入的Monitor类型不正确，类型有TCP,HTTP,HTTPS,请输入正确的Monitor类型！！！")


# F5,CM类，用于同步双机配置。
class F5CMSYNCClass(F5CONNClass):
    # 链接F5设备，并对函数进行赋值；Deviceip为设备IP地址，Username为设备用户名，Password为设备密码。默认端口号为：443.
    def __init__(self, deviceip, username, password):
        F5CONNClass.__init__(self, deviceip, username, password)
        self.device_groups = self.mgmt.tm.cm.device_groups
        self.device_group = self.mgmt.tm.cm.device_groups.device_group

    # 获取设备同步组的名称列表。
    def getDeviceName(self):
        device_collection = self.device_groups.get_collection()
        devicelist = []
        for device in device_collection:
            devicelist.append(device.name)
        self.devicelist = devicelist
        return self.devicelist

    # 配置由设备同步到组。同步名称为同步组的名称，就是设备WEB界面下，
    # 设备管理下的DEVICE GROUPS下自定义的名称，不是单个设备的名称，设备同步组的列
    # 表可以通过getDeviceName()函数获得。通过与自己的设备对应即可。下列函数DEVICENAME的名称即为
    def syncDeviceToGroup(self, devicename):
        if self.device_group.exists(name=devicename) == True:
            devicesync = self.device_group.load(name=devicename)
            devicesync.sync_to()
            print(">>>同步设备配置到同步组成功！！！")
        else:
            print(">>>同步组名称：" + devicename + "不存在，请检查配置文件！！！")

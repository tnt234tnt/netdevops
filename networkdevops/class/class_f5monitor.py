#该函数用于新建MONITOR，查看MONITOR状态等。
import f5.bigip
from f5.bigip import ManagementRoot
import class_f5conn
from class_f5conn import F5CONNClass

#定义Monitor类，继承父类f5ltmclass，
class F5MONITORClass(F5CONNClass):

#初始化函数
    def __init__(self,deviceip,username,password):
        F5CONNClass.__init__(self,deviceip,username,password)
        self.http = self.mgmt.tm.ltm.monitor.https.http
        self.https = self.mgmt.tm.ltm.monitor.https_s.https
        self.tcp = self.mgmt.tm.ltm.monitor.tcps.tcp
        self.monitor = self.mgmt.tm.ltm.monitor
        
#新建MONITOR，类型为三类，TCP,HTTP,HTTPS，其他的利用率不高，就不做了。
#输入的参数有5个，monitortype为要新建的Monitor类型，TCP/HTTP/HTTPS，monitorname为要新建的monitor名称，send为要发送的消息，recv为返回的消息，recvDisable为失败返回的消息，一般用不到！
    recvmsg = {'recvDisable':None}
    def createMonitor(self,monitortype,monitorname,send,recv,**recvmsg):
        http = self.http
        https = self.https
        tcp = self.tcp
#首先检查输入的监控类型，根据类型添加相应的MONITOR。
        if monitortype == 'tcp':
            if tcp.exists(name = monitorname) == True:
                print(">>>TcpMonito" + monitorname + "已经存在，请检查配置文件！！！")
            else:
                tcpmonitor = tcp.create(name = monitorname,send = send , recv = recv , **recvmsg)
                print(">>>TcpMonito" +  monitorname + "创建成功！！！")
        elif monitortype == 'http':
            if http.exists(name = monitorname) == True:
                print(">>>HttpMonito" + monitorname + "已经存在，请检查配置文件！！！")
            else:
                httpmonitor = http.create(name = monitorname,send = send , recv = recv , **recvmsg)
                print(">>>HttpMonito" +  monitorname + "创建成功！！！")                
        elif monitortype == 'https':
            if https.exists(name = monitorname) == True:
                print(">>>HttpsMonito" + monitorname + "已经存在，请检查配置文件！！！")
            else:
                httpsmonitor = https.create(name = monitorname,send = send , recv = recv , **recvmsg)
                print(">>>HttpsMonito" +  monitorname + "创建成功！！！")                                
        else:
            print(">>>您输入的Monitor类型不正确，支持的类型有TCP,HTTP,HTTPS,请输入前3种类型的Monitor类型！！！")
    
#获取所有MONITOR的名字。包含TCP/HTTP/HTTPS。
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
        return self.monitorhttplist,self.monitorhttpslist,self.monitortcplist
    
#分别获取指定类型的Monitor列表。参数为TCP/HTTP/HTTPS，仅支持3种。
    def getMonitor(self,monitortype):
        if monitortype == 'tcp':
            return self.monitortcplist
        elif monitortype == 'http':
            return self.monitorhttplist
        elif monitortype == 'https':
            return self.monitorhttpslist
        else:
            print(">>>您输入的Monitor类型不正确，类型有TCP,HTTP,HTTPS,请输入正确的Monitor类型！！！")
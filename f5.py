mport f5.bigip
from f5.bigip import ManagementRoot
#连接F5设备
mgmt = ManagementRoot('192.168.1.1', 'admin', 'admin')
#新建POOL
pool1 = mgmt.tm.ltm.pools.pool.create(name='pool1', partition='Common')
#加载POOL信息
pool_obj = mgmt.tm.ltm.pools.pool
pool_1 = pool_obj.load(partition='Common', name='pool1')
#添加POOL备注
pool_1.description = "This is my pool"
pool_1.update()

#新建POOL1的member
m1 = pool_1.members_s.members.create(partition='Common', name='192.168.101.50:80')
m2 = pool_1.members_s.members.create(partition='Common', name='192.168.101.51:80')


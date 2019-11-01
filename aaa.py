import f5.bigip
from f5.bigip import ManagementRoot
#连接F5设备
mgmt = f5.bigip.ManagementRoot('10.99.100.41', 'admin', 'Admin@123')
#新建POOL
pool1 = mgmt.tm.ltm.pools.pool.create(name='pool9',monitor = 'tcp',description="This is My Python pool!",partition='Common')
#加载POOL信息
pool_1 = mgmt.tm.ltm.pools.pool.load(partition='Common', name='pool1')

#添加POOL备注
pool_1.description = "This is my pool"
pool_1.update()

#新建POOL1的member
m1 = pool_1.members_s.members.create(partition='Common', name='192.168.101.50:80')
m2 = pool_1.members_s.members.create(partition='Common', name='192.168.101.51:80')

#新建VS
mgmt.tm.ltm.virtuals.virtual.create(name='vs1',partition='Common',pool = 'pool1',destination = '195.1.1.1:80',ipProtocol = 'tcp',mask = '255.255.255.255')
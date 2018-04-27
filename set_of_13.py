import os

os.system("ovs-vsctl set Bridge s1 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s2 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s3 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s4 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s5 protocols=OpenFlow13")


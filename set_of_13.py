import os
import subprocess

os.system("ovs-vsctl set Bridge s1 protocols=OpenFlow13")
os.system("ovs-vsctl set-manager ptcp:6632")

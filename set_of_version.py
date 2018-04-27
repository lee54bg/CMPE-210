"""

Ensure rest_topology is running after executing your topology before running this program
as this gets the list of switches (datapath ids) and sets the openflow version
accordingly

"""

import os
import subprocess

switch_list = []

output = subprocess.check_output("ovs-vsctl list-br", shell=True)

print(type(output))

for data in output.splitlines():
    set_of_vers = "ovs-vsctl set Bridge {0} protocols=OpenFlow13".format(data)

    print(set_of_vers)

    os.system(set_of_vers)
    # switch_list.append(data)
    # print(data)



"""
os.system("ovs-vsctl set Bridge s1 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s2 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s3 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s4 protocols=OpenFlow13")
os.system("ovs-vsctl set Bridge s5 protocols=OpenFlow13")
"""

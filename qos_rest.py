import json
import requests

print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))


def acqSwitchInfo(url, switch_info):
    switch = requests.put(url, data=switch_info)

def install_qos_rules(url, data=None):
    '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "500000"}, {"min_rate": "800000"}]}'
    enable_queue = requests.post(url, data)
    print(enable_queue)
    enable_queue.content
# acqSwitchInfo("http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr", '"tcp:127.0.0.1:6632"')

install_qos_rules("http://localhost:8080/qos/queue/0000000000000001", '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "500000"}, {"min_rate": "800000"}]}')


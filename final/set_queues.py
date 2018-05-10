import json
import requests
import time

def get_qos_settings():
    connection = '"tcp:127.0.0.1:6632"'
    switch_addr = "http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr"
    ovsdb_access = requests.put(switch_addr, connection)

    time.sleep(2)
    qos_rules = '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues":[{"max_rate": "200000"}, {"max_rate": "500000"}, {"min_rate": "800000"}]}'

    post_queues = requests.post("http://localhost:8080/qos/queue/0000000000000001", qos_rules)

    print(post_queues)
    print(json.loads(post_queues.content))
    print("\n")
get_qos_settings()

import json
import requests
import time

def get_qos_settings():
    connection = '"tcp:127.0.0.1:6632"'
    switch_addr = "http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr"
    ovsdb_access = requests.put(switch_addr, connection)

    time.sleep(2)
"""
    qos_rules = '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues":[{"max_rate": "1000000"}, {"min_rate": "200000"}, {"min_rate": "500000"}]}'

    post_queues = requests.post("http://localhost:8080/qos/queue/0000000000000001", qos_rules)

    print(post_queues)
    print(json.loads(post_queues.content))
"""
    dict_items = {
        '{"address": "172.16.20.1/24"}': "http://localhost:8080/router/0000000000000001",
        '{"address": "172.16.30.10/24"}': "http://localhost:8080/router/0000000000000001",
        '{"gateway": "172.16.30.1"}': "http://localhost:8080/router/0000000000000001",
        '{"address": "172.16.10.1/24"}': "http://localhost:8080/router/0000000000000002",
        '{"address": "172.16.30.1/24"}': "http://localhost:8080/router/0000000000000002",
        '{"gateway": "172.16.30.10"}': "http://localhost:8080/router/0000000000000002"
    }

    for key, value in dict_items.items():
        status = requests.post(value, key)
        print(status)
"""
    switch_addr = "http://localhost:8080/qos/rules/0000000000000001"
    queue_one = '{"match": {"ip_dscp": "26"}, "actions":{"queue": "1"}}'
    queue_two = '{"match": {"ip_dscp": "34"}, "actions":{"queue": "2"}}'

    q1 = requests.post(switch_addr, queue_one)
    print(q1)
    q2 = requests.post(switch_addr, queue_two)
    print(q2)
"""
get_qos_settings()


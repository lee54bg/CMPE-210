import json
import requests
import time

def get_qos_settings():
    connection = '"tcp:127.0.0.1:6632"'
    switch_addr = "http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr"
    ovsdb_access = requests.put(switch_addr, connection)

    time.sleep(2)
    qos_rules = '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues":[{"max_rate": "1000000"}, {"min_rate": "200000"}, {"min_rate": "500000"}]}'

    post_queues = requests.post("http://localhost:8080/qos/queue/0000000000000001", qos_rules)

    switch_addr = "http://localhost:8080/qos/rules/0000000000000001"
    switch_addr_2 = "http://localhost:8080/qos/rules/0000000000000002"
    queue_one = '{"match": {"ip_dscp": "26"}, "actions":{"queue": "1"}}'
    queue_two = '{"match": {"ip_dscp": "34"}, "actions":{"queue": "2"}}'

    q1 = requests.post(switch_addr, queue_one)
    print(q1)
    print(q1.content)
    q2 = requests.post(switch_addr, queue_two)
    print(q2)
    print(q2.content)
"""
    m2 = requests.post(switch_addr_2, '{"match": {"nw_dst": "10.0.0.1", "tp_dst": "5002"}, "actions":{"mark": "26"}}')
    print(m2)
    print(m2.content)
    m1 = requests.post(switch_addr_2, '{"match": {"nw_dst": "10.0.0.1", "tp_dst": "5003"}, "actions":{"mark": "34"}}')
    print(m1)
    print(m1.content)
"""
get_qos_settings()


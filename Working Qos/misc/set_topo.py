import json
import requests

def get_qos_settings():
    qos_rules = '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues":[{"max_rate": "1000000"}, {"min_rate": "200000"}, {"min_rate": "500000"}]}'

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

get_qos_settings()


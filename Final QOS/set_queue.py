import json
import requests

def get_qos_settings():
    qos_rules = '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues":[{"max_rate": "1000000"}, {"min_rate": "200000"}, {"min_rate": "500000"}]}'
    post_queues = requests.post("http://localhost:8080/qos/queue/0000000000000001", qos_rules)

    print(post_queues)
    print(json.loads(post_queues.content))
    print("\n")
get_qos_settings()


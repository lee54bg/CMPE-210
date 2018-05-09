import requests
import json

def get_qos_settings():
    set_ovsdb = requests.put("http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr", '"tcp:127.0.0.1:6632"')
    print("db")
    print(set_ovsdb)

    post_queue = requests.post("http://localhost:8080/qos/queue/0000000000000001", '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "300000"}, {"max_rate": "500000"}, {"min_rate": "800000"}]}')
    queue = json.loads(post_queue.content)

    print("Print queues")
    get_queue = requests.get("http://localhost:8080/qos/queue/0000000000000001")
    queue_list = json.loads(get_queue.content)
    print(queue_list)

    qos_rule = requests.post("http://localhost:8080/qos/rules/0000000000000001", '{"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5003"}, "actions":{"queue": "2"}}')
    print(qos_rule)

    print("Print queues")
    get_queue = requests.get("http://localhost:8080/qos/queue/0000000000000001")
    queue_list = json.loads(get_queue.content)
    print(queue_list)
get_qos_settings()


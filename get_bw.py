
import json
import requests

# print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))

def get_qos_settings(switch_id):
    http_req = "http://localhost:8080/qos/queue/" + str(switch_id)
    switch_settings = requests.get(http_req)

    json_switch_settings = json.loads(switch_settings.content)

    # For switches that have queues on them
    queue_list = json_switch_settings[0]['command_result']['details']['s1-eth1']
    print(queue_list)

    for key, value in queue_list.items():
	configs = queue_list[key]['config']
	print(configs)
	if "max-rate" in configs:
	    print(configs['max-rate'])
	# key['config']


get_qos_settings("0000000000000001")


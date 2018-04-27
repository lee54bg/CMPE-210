
import json
import requests

# print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))

def get_qos_settings(switch_id):
    http_req = "http://localhost:8080/qos/rules" + str(switch_id)
    switch_settings = requests.get(http_req)
    print(switch_settings)
    print(switch_settings.content)

    # json_switch_settings = json.loads(switch_settings)
    # print(json_switch_settings)

    
get_qos_settings("http://localhost:8080/qos/rules/0000000000000001")


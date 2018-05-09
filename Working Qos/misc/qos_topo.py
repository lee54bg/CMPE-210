
import json
import requests

# print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))

def get_qos_settings(switch_id):
    http_req = "http://localhost:8080/v1.0/topology/switches" + str(switch_id)
    switch_settings = requests.get(http_req)
    
    json_switch_settings = json.loads(switch_settings.content)
    # print(json_switch_settings)

    switch_list = []
  
    for i in range(len(json_switch_settings)):
	switch_list.append(json_switch_settings[i]['ports'][0]['dpid'])
        print(json_switch_settings[i]['ports'][0]['dpid'])
        ovsdb_on = "http://localhost:8080/v1.0/conf/switches/" + switch_list[i] + "/ovsdb_addr" 
    
    # print(type(json_switch_settings))
    # print(json_switch_settings[0]['ports'])
    
    print("Printing DPID")
    print(json_switch_settings[0]['ports'][0]['dpid'])
    
    # new_string = json.dumps(json_switch_settings, indent=2)
    # for data in json_switch_settings:
    
get_qos_settings("")


from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
import requests
import json

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


	# Indicates an empty match which means that we match everything
        match = parser.OFPMatch()
	# Forward the packet to the OF Controller without buffering
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
	# Call add_flow to install flow entry via flow_mod to modify flow table
	# To add flow entry
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, table_id=1)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, table_id=1)
        datapath.send_msg(mod)

    def drop_flow(self, datapath, priority, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_CLEAR_ACTIONS, [])]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst, table_id=1)
        datapath.send_msg(mod)



    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
	eth = pkt.get_protocols(ethernet.ethernet)[0]
	ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
	arp_pkt = pkt.get_protocol(arp.arp)

	if ipv4_pkt:
	    ipv4_src = ipv4_pkt.src
	    print(ipv4_src)
	elif arp_pkt:
	    arp_src_ip = arp_pkt.src_ip
	    print(arp_src_ip)

        dst = eth.dst
        src = eth.src

	# Define a list of subscribers	
	eth_list = ["00:00:00:00:00:02", "00:00:00:00:00:03", "00:00:00:00:00:05", "00:00:00:00:00:01"]
	found = False
	# Check list to see if MAC address is found in the list of MAC address	
	if src in eth_list:
	    # Execute the set_qos function to install qos rules
	    self.set_qos(src)
	    print("Success")
	    found = True
	
	# Otherwise, install a flow rule that essentially drops the packet 
	# by calling the drop_flow method
	if found == False:
	    match = parser.OFPMatch(eth_src = src)
	    self.drop_flow(datapath, 0, match)
	    return
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
        
	if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    # Function used to set the QoS rules when there's a match
    def set_qos(self, eth_src):
	if eth_src == "00:00:00:00:00:02":
            first_rule = requests.post("http://localhost:8080/qos/rules/0000000000000001", '{"match": {"nw_src": "10.0.0.2", "nw_dst": "10.0.0.1"}, "actions":{"queue": "1"}}')
            
	if eth_src == "00:00:00:00:00:03":
            third_rule = requests.post("http://localhost:8080/qos/rules/0000000000000001", '{"match": {"nw_src": "10.0.0.3", "nw_dst": "10.0.0.1"}, "actions":{"queue": "2"}}')


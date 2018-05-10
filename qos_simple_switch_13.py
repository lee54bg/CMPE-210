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
        # If a buffer ID has been provided, then install the
        # flow entry with the buffer IP
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, table_id=1)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, table_id=1)
        datapath.send_msg(mod)

    # Drop flow entries
    def drop_flow(self, datapath, priority, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Initiate the instructions to be empty.  By default, an empty action
        # consistitutes an automatic drop of a packet
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_CLEAR_ACTIONS, [])]

        # Message sent to the switch to modify the flow table
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst, table_id=1)
        datapath.send_msg(mod)

    # Our event handler to handle packet-in messages.
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Initialize empty IPv4 variables
        arp_src_ip = None
        arp_dst_ip = None
        ip4_src = None
        ip4_dst = None

        # Used to check if IP address is in the list of subscribers
        found = False

        # Get the full packet with all the protocols embedded in the
        # packet
        pkt = packet.Packet(msg.data)
	eth = pkt.get_protocols(ethernet.ethernet)[0]
        # Extract ARP and IPv4 packet simultaneously
        arp_pkt = pkt.get_protocol(arp.arp)
	ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
	
        src = eth.src
        dst = eth.dst
        
        # Define a list of subscribers IP
        ip_list = ["10.0.0.2", "10.0.0.3", "10.0.0.5"]
        
	# Check to see if an ARP packet exists.  If not, use the IPv4 packet instead
	# Afterwards, check to ensure that the IP address in question is listed
	# in the subscriber list.  If not, then we drop the packet-in
        if arp_pkt:
	    arp_src_ip = arp_pkt.src_ip
            arp_dst_ip = arp_pkt.dst_ip
	    
	    if arp_src_ip in ip_list:
                print("Subscriber in list: ")
                print(arp_src_ip)
                found = True
                # self.set_qos(arp_pkt)
            elif arp_dst_ip in ip_list:
                found = True
            else:
                match = parser.OFPMatch(arp_spa = arp_src_ip)
                self.drop_flow(datapath, 0, match)
                return
	elif ipv4_pkt:
	    ip4_src = ipv4_pkt.src
	    ip4_dst = ipv4_pkt.dst
	    # print(ipv4_src)
            
	    if ip4_src in ip_list:
                print("Subscriber in list: ")
                found = True
                # self.set_qos(ipv4_pkt)
            elif ip4_dst in ip_list:
                found = True
            else:
                match = parser.OFPMatch(ipv4_src = ip4_src)
                self.drop_flow(datapath, 0, match)
                return

	dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
        
	if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # Set action to forward packet-in message to the output port.
        actions = [parser.OFPActionOutput(out_port)]

        # Install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port = in_port, eth_dst = dst, eth_src = src)

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
        # Send the message to the controller
        datapath.send_msg(out)


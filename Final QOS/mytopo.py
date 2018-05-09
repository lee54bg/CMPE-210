from mininet.topo import Topo

class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        self.addLink(h1, s1)
        self.addLink(s2, h2)
        self.addLink(s2, h3)
        self.addLink(s2, h4)
        self.addLink(s2, s1)

        s1.cmd("ovs-vsctl set Bridge s1 protocols=OpenFlow13")
        s1.cmd("ovs-vsctl set-manager ptcp:6632")
        s2.cmd("ovs-vsctl set Bridge s2 protocols=OpenFlow13")

        h1.cmd("ip addr del 10.0.0.1/8 dev h1-eth0")
        h1.cmd("ip addr add 172.16.20.10/24 dev h1-eth0")

        h2.cmd("ip addr del 10.0.0.2/8 dev h2-eth0")
        h2.cmd("ip addr add 172.16.10.10/24 dev h2-eth0")

        c0 = net.get('c0')

        h1.cmd("ip route add default via 172.16.20.1")
        h2.cmd("ip route add default via 172.16.10.1")
topos = {'mytopo':(lambda:MyTopo())}

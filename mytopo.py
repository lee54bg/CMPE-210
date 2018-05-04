from mininet.topo import Topo

class MyTopo(Topo):

        def __init__(self):
                Topo.__init__(self)
                host1 = self.addHost('h1',ip="172.16.20.10",defaultRoute = "via 172.16.20.1")
                host2 = self.addHost('h2',ip="172.16.10.10",defaultRoute = "via 172.16.20.1")
                host3 = self.addHost('h3',ip="172.16.30.10",defaultRoute = "via 172.168.20.1")
                host4 = self.addHost('h4',ip="172.16.40.10",defaultRoute = "via 172.168.20.1")
                switch1 = self.addSwitch('s1')
                switch2 = self.addSwitch('s2')

                self.addLink(switch1, host1)
                self.addLink(switch2, host3)
                self.addLink(switch2, host4)
                self.addLink(switch2, host2)
                self.addLink(switch1, switch2)

topos = {'mytopo':(lambda:MyTopo())}



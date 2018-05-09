from mininet.topo import Topo

class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')

        self.addLink(h1, s1)
        self.addLink(s1, h2)
        self.addLink(s1, h3)
        self.addLink(s1, h4)
        
topos = {'mytopo':(lambda:MyTopo())}

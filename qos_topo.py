from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def multiControllerNet():
    net = Mininet(switch=OVSSwitch )

    c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    s1 = net.addSwitch('s1')

    net.addLink(h1, s1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)
    
    net.build()
    c0.start()
    s1.start([c0])

    s1.cmd("ovs-vsctl set Bridge s1 protocols=OpenFlow13")
    s1.cmd("ovs-vsctl set-manager ptcp:6632")

    CLI( net )

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    multiControllerNet()


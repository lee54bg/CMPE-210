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
    s2 = net.addSwitch('s2')

    net.addLink(h1, s1)
    net.addLink(s2, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s2, s1)

    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])

    s1.cmd("ovs-vsctl set Bridge s1 protocols=OpenFlow13")
    s1.cmd("ovs-vsctl set-manager ptcp:6632")
    # s1.cmd("curl -X POST -d '{\"match\": {\"ip_dscp\": \"0\", \"in_port\": \"2\"}, \"actions\":{\"queue\": \"1\"}}' http://localhost:8080/qos/rules/0000000000000001")
    s2.cmd("ovs-vsctl set Bridge s2 protocols=OpenFlow13")

    h1.cmd("ip addr del 10.0.0.1/8 dev h1-eth0")
    h1.cmd("ip addr add 172.16.20.10/24 dev h1-eth0")

    h2.cmd("ip addr del 10.0.0.2/8 dev h2-eth0")
    h2.cmd("ip addr add 172.16.10.10/24 dev h2-eth0")

    h3.cmd("ip addr del 10.0.0.3/8 dev h3-eth0")
    h3.cmd("ip addr add 172.16.10.11/24 dev h3-eth0")

    h4.cmd("ip addr del 10.0.0.4/8 dev h4-eth0")
    h4.cmd("ip addr add 172.16.10.12/24 dev h4-eth0")

    # h1.cmd("ip route add default via 172.16.20.1")
    # h2.cmd("ip route add default via 172.16.10.1")

    CLI( net )

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    multiControllerNet()

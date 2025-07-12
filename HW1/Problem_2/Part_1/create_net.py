from mininet .net import Mininet
from mininet .node import RemoteController , OVSKernelSwitch
from mininet .cli import CLI
from mininet .log import setLogLevel
from mininet .link import TCLink

def topol():

    net = Mininet( controller=RemoteController,link= TCLink,switch = OVSKernelSwitch ,autoSetMacs=True)

    #Hosts
    h1 = net.addHost(name = 'h1',ip='10.0.0.1')
    h2 = net.addHost(name = 'h2',ip='10.0.0.2')
    h3 = net.addHost(name = 'h3',ip='10.0.0.3')
    h4 = net.addHost(name = 'h4',ip='10.0.0.4')
    h5 = net.addHost(name = 'h5',ip='10.0.0.5')
    h6 = net.addHost(name = 'h6',ip='10.0.0.6')
    h7 = net.addHost(name = 'h7',ip='10.0.0.7')
    h8 = net.addHost(name = 'h8',ip='10.0.0.8')
    #Switches
    s1 = net.addSwitch('s1',protocols="OpenFlow13")
    s2 = net.addSwitch('s2',protocols="OpenFlow13")
    s3 = net.addSwitch('s3',protocols="OpenFlow13")
    s4 = net.addSwitch('s4',protocols="OpenFlow13")
    s5 = net.addSwitch('s5',protocols="OpenFlow13")
    s6 = net.addSwitch('s6',protocols="OpenFlow13")
    s7 = net.addSwitch('s7',protocols="OpenFlow13")
    #links
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)
    net.addLink(s4, h7)
    net.addLink(s4, h8)
    net.addLink(s1, s5)
    net.addLink(s2, s5)
    net.addLink(s3, s6)
    net.addLink(s4, s6)
    net.addLink(s5, s7)
    net.addLink(s6, s7)
    #controller and its initialization
    C1 = net.addController(name='c1',ip='192.168.17.129',port=6653)
    s1.start([C1])
    s2.start([C1])
    s3.start([C1])
    s4.start([C1])
    s5.start([C1])
    s6.start([C1])
    s7.start([C1])
    net.build()
    net.start()
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    topol()
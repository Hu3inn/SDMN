from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet .link import TCLink

def topology():
    net = Mininet(
        controller=None,
        switch=OVSKernelSwitch,
        link= TCLink
    )
    
    # Adding hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24', mac= '00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac= '00:00:00:00:00:02')
    
    # Adding switch
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    # Adding links
    net.addLink(s1,h1)
    net.addLink(s2,h2)
    net.addLink(s1, s2)
    
    # Start network
    net.build()
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
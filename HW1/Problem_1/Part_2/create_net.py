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
    h1 = net.addHost( name='h1', ip='10.0.1.1/24', mac= '00:00:00:00:00:01', defaultRoute='via 10.0.1.1')
    h2 = net.addHost( name='h2', ip='10.0.2.1/24', mac= '00:00:00:00:00:02', defaultRoute='via 10.0.2.1')

    
    # Adding switches and router
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3', mac= '00:00:00:00:00:03')  # Router is just another OVS switch (I tried to use r1 to distinguish it but it gives me error so i used s3)
    
    # Adding links
    net.addLink(s1, h1)
    net.addLink(s2, h2)
    net.addLink(s1, s3)
    net.addLink(s2, s3)
    
    # Start network
    net.build()
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
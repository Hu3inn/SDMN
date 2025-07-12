from mininet .net import Mininet
from mininet .node import RemoteController , OVSKernelSwitch
from mininet .cli import CLI
from mininet .log import setLogLevel
from mininet .link import TCLink
from create_flows import switch_xml, router_xml

def topol():

    net = Mininet(controller=RemoteController, link= TCLink,switch = OVSKernelSwitch )

    h1 = net.addHost( name='h1', ip='10.0.1.1/24', mac= '00:00:00:00:00:01', defaultRoute='via 10.0.1.10')
    h2 = net.addHost( name='h2', ip='10.0.2.1/24', mac= '00:00:00:00:00:02', defaultRoute='via 10.0.2.10')


    s1 = net.addSwitch('s1',protocols='OpenFlow13')
    s2 = net.addSwitch('s2',protocols='OpenFlow13')
    s3 = net.addSwitch('s3',mac= '00:00:00:00:00:03',protocols='OpenFlow13')
    
    
    net.addLink(s1,s3)
    net.addLink(s2,s3)
    
    
   

    c1 = net.addController(name='c1',ip='192.168.17.129',port=6653,protocols='OpenFlow13')
    
    # links
    net.addLink(s1,h1)
    net.addLink(s2,h2)


    s1.start([c1])
    s2.start([c1])
    s3.start([c1])

    net.build()
    net.start()

    

    h2.cmd('arp -s 10.0.2.10 00:00:00:00:00:03')
    h1.cmd('arp -s 10.0.1.10 00:00:00:00:00:03')

    ###
    #openflow:1
    switch_xml(1,1,'00:00:00:00:00:03',1)
    switch_xml(1,2,'00:00:00:00:00:01',2)


    #openflow:2
    switch_xml(2,1,'00:00:00:00:00:02',2)
    switch_xml(2,2,'00:00:00:00:00:03',1)


    #openflow:3
    router_xml(3,1,'10.0.2.0/24','00:00:00:00:00:02',2)
    router_xml(3,2,'10.0.1.0/24','00:00:00:00:00:01',1)
    ###

    
    CLI( net )
    #deleting all switches flows in order for the new rules update successfuly
    #alternatively you can comment out "from create_flows" line 6 and and cut the
    #lines I put between two ### and paste it at the end of create_flow, then 
    #run it at another terminal before push_flows
    s1.dpctl('del-flows', '-O', 'OpenFlow13')
    s2.dpctl('del-flows', '-O', 'OpenFlow13')
    s3.dpctl('del-flows', '-O', 'OpenFlow13')

    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    topol()

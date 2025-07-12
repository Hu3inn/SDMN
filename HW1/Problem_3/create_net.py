from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

from create_flows import Flow_Maker
from spf import best_Path

def topol():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)
    mat = [[0,2,3,4],[2,0,0,1],[3,0,0,0],[1,1,0,0]] 
    NumOfNodes = len(mat)
    Path_d = best_Path(mat,1,4)
    portList = []
    for i in range(NumOfNodes):
        portList.append([])
    switches = [ net.addSwitch( 's%s' % s,mac='00:00:00:00:0{}:00'.format(s),protocols='OpenFlow13')
                     for s in range( 1,NumOfNodes+1) ]  
    sw_Actint = {}  
    for sw in switches:
        sw_Actint[sw]=1
    Llist = []     
    h1 = net.addHost( name='h1', ip='10.0.1.1/24', mac= '10:00:00:00:00:01',defaultRoute='via 10.0.1.10')
    h2 = net.addHost( name='h2', ip='10.0.2.1/24', mac= '20:00:00:00:00:02',defaultRoute='via 10.0.2.10')  
 
    sw_Actint[switches[0]] += 1
    sw_Actint[switches[NumOfNodes-1]] += 1           
    net.addLink(h1, switches[0])
    net.addLink(h2, switches[NumOfNodes-1])        
    
    for j in range(len(mat)):
        for i in range(len(mat[j])):
            L_cost = mat[j][i]
            if (L_cost != 0) and ('{} {}'.format(i, j) not in Llist) :
                Llist.append('{} {}'.format(j, i))
                net.addLink(switches[j], switches[i])
                sw_Actint[switches[i]] += 1
                sw_Actint[switches[j]] += 1
                
    for j in range(len(mat)):
        if j == 0 or j == NumOfNodes -1 :
            interface_idx = 2
        else :
            interface_idx = 1
        for i in range(len(mat[j])):
            if mat[j][i] != 0:
                portList[j].append(interface_idx)
                interface_idx += 1 
            else : 
                portList[j].append(0)
         

    c1 = net.addController(name='c1',ip='192.168.17.129',port=6633,protocols='OpenFlow13')
    for sw_index in range(NumOfNodes):
        switches[sw_index].start([c1])
        
    Flow_Maker(NumOfNodes,Path_d,portList)
    
    net.build()
    
    net.start()

    
    h2.cmd('arp -s 10.0.2.10 00:00:00:00:04:00')
    h1.cmd('arp -s 10.0.1.10 00:00:00:00:03:00')
      
    
    CLI( net )
    '''for swit in range(NumOfNodes):
        switches[swit].dpctl('del-flows', '-O', 'OpenFlow13')'''
    switches[0].dpctl('del-flows', '-O', 'OpenFlow13')
    switches[1].dpctl('del-flows', '-O', 'OpenFlow13')
    switches[2].dpctl('del-flows', '-O', 'OpenFlow13')
    switches[3].dpctl('del-flows', '-O', 'OpenFlow13')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topol()

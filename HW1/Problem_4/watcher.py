from create_flows import Flow_Maker
from spf import best_Path
from time import sleep
import requests
import json
from requests.auth import HTTPBasicAuth
from os import remove
import send_flows
import glob

flag = False

def cleaning():
    # deleting all the flows that are located in Flow folder   
    # and also clearing the ones in all of the devices 
    files = glob.glob('./flow/*')
    for f in files:
        remove(f)

def CheckTheState(N, CostMat, PortMat):
    global flag
    linksd = {}
    header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    for i in range(1, N + 1):
        url = "http://192.168.17.129:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:{}/".format(i)
        data = requests.get(url, headers=header, auth=('admin', 'admin'), verify=False)
        rdt = data.json()
        nlen = len(rdt['node'][0]['node-connector'])
        for j in range(0, nlen):
            linkn = rdt['node'][0]['node-connector'][j]['flow-node-inventory:name']
            links = rdt['node'][0]['node-connector'][j]['flow-node-inventory:state']['link-down']
            linksd[linkn] = links

    if RoutingCalc(N, CostMat, PortMat, linksd) == True:
        flag = True

def RoutingCalc(N, CostMat, PortMat, linkStates):
    devs = []
    for key in linkStates.keys():
        if 'eth' in str(key):
            if linkStates[key] == True:
                dev_port = str(key)
                parts = dev_port.split('-')
                if len(parts) == 2 and parts[0].startswith('s') and parts[1].startswith('eth'):
                    dev = parts[0][1:]  # remove 's', keep number
                    port = parts[1][3:] # remove 'eth', keep number
                    print('dev_port  : s{} , {}'.format(dev, port))
                    devs.append([dev, port])
                else:
                    print("Skipping malformed dev_port:", dev_port)

                '''dev_port = str(key)
                port = str(dev_port.split('-')[1][3:])
                dev = str(dev_port.split('-')[0][2:])'''
                print('dev_port  : s{} , {}'.format(dev, port))
                devs.append([dev, port])
    if devs != []:
        CostMat[int(devs[0][0]) - 1][int(devs[1][0]) - 1] = 0
        CostMat[int(devs[1][0]) - 1][int(devs[0][0]) - 1] = 0
        PortMat[int(devs[0][0]) - 1][int(devs[1][0]) - 1] = 0
        PortMat[int(devs[1][0]) - 1][int(devs[0][0]) - 1] = 0
        Path_dij = best_Path(CostMat, 1, N)
        print('updating flows')
        cleaning()
        Flow_Maker(N, Path_dij, PortMat)
        send_flows.PushFlows(N)
        return True
    return False


mat = [[0, 2, 3, 4], [2, 0, 0, 1], [3, 0, 0, 0], [1, 1, 0, 0]] 
N = len(mat)
CostMat = mat[:]  # shallow copy for Python 2
PortMat = [[0, 2, 3, 4], [1, 0, 0, 2], [1, 0, 0, 0], [2, 3, 0, 0]]

time_interval = 5  # seconds

while True:
    print("checking...")
    sleep(time_interval)
    if flag == False:
        CheckTheState(N, CostMat, PortMat)

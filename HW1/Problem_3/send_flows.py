import requests
from requests.auth import HTTPBasicAuth
from os.path import isfile

def dev_flows(NumberofNODES):
    devices = {}
    path_file = "./flow/openflow1:id_1.xml"
    id_counter = 1 
    of_counter = 1 
    while of_counter <= NumberofNODES:
        devices[of_counter] = 0
        while isfile(path_file):
            devices[of_counter] += 1
            id_counter += 1
            path_file = "./flow/openflow{}:id_{}.xml".format(of_counter, id_counter)
        id_counter = 1
        of_counter += 1
        path_file = "./flow/openflow{}:id_{}.xml".format(of_counter, id_counter)
    return devices    

def PushFlows(N):
    Header = {'Accept': 'application/xml', 'Content-Type': 'application/xml'} 
    devices = dev_flows(N)
    for openflowID in devices.keys():
        for flow_x in range(1, devices[openflowID] + 1):
            URL = 'http://192.168.17.129:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/0/flow/{}'.format(openflowID, flow_x)
            file_addr = './flow/openflow{}:id_{}.xml'.format(openflowID, flow_x)
            f = open(file_addr, "rb")
            xml_raw = f.read()
            f.close()
            code = requests.put(URL, headers=Header, data=xml_raw, auth=HTTPBasicAuth('admin', 'admin')).status_code
            print(code)


PushFlows(4)

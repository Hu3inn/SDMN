import requests
from requests.auth import HTTPBasicAuth

Header = {'Accept': 'application/xml', 'Content-Type': 'application/xml'} 
devices = {1: 2, 2: 2, 3: 2}

for openflowID in devices.keys():
    for flow_x in range(1, devices[openflowID] + 1):
        URL = 'http://192.168.17.129:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/0/flow/{}'.format(openflowID, flow_x)
        file_addr = './flow/openflow{}:id_{}.xml'.format(openflowID, flow_x)
        # print('file address {}\n'.format(file_addr))
        f = open(file_addr, "rb")
        xml_raw = f.read()
        f.close()
        # print('xml_raw {}\n'.format(file_addr))
        # print(xml_raw)
        # print('---------------------------------------------------------')
        code = requests.put(URL, headers=Header, data=xml_raw, auth=HTTPBasicAuth('admin', 'admin')).status_code
        print(code)


            
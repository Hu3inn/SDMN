#!/usr/bin/python2
import urllib2
import base64
import os

# Configuration
ODL_IP = '192.168.17.129'
ODL_PORT = '8181'
USERNAME = 'admin'
PASSWORD = 'admin'
FLOW_DIR = './Flow'

# Create basic auth header
auth_string = base64.b64encode('{}:{}'.format(USERNAME, PASSWORD))
headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
    'Authorization': 'Basic {}'.format(auth_string)
}

devices = {1: 2, 2: 2, 3: 2}  # {switch_id: number_of_flows}

def push_flow(switch_id, flow_id):
    url = 'http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/0/flow/{}'.format(
        ODL_IP, ODL_PORT, switch_id, flow_id)
    file_path = '{}/openflow{}:id_{}.xml'.format(FLOW_DIR, switch_id, flow_id)
    
    try:
        with open(file_path, 'rb') as f:
            xml_data = f.read()
        
        request = urllib2.Request(url, data=xml_data, headers=headers)
        request.get_method = lambda: 'PUT'  # Make it a PUT request
        
        try:
            response = urllib2.urlopen(request)
            print('Success! Switch: openflow:{}, Flow: {} - Status: {}'.format(
                switch_id, flow_id, response.getcode()))
            print('Response: {}'.format(response.read()))
        except urllib2.HTTPError as e:
            print('Failed! Switch: openflow:{}, Flow: {}'.format(switch_id, flow_id))
            print('Error code: {}'.format(e.code))
            print('Error response: {}'.format(e.read()))
            
    except IOError as e:
        print('File error for openflow{}:id_{}.xml: {}'.format(switch_id, flow_id, str(e)))

# Main execution
for switch_id, flow_count in devices.items():
    for flow_num in range(1, flow_count + 1):
        push_flow(switch_id, flow_num)
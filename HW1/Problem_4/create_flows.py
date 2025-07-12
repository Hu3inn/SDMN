def switch_xml(openflow_num, flow_id, dst_net, out_port):
    raw_body = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <barrier>false</barrier>
    <cookie>8</cookie>
    <id>{}</id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                    <dec-nw-ttl/>
                </action>
                <action>
                    <order>1</order>
                    <output-action>
                        <output-node-connector>{}</output-node-connector>
                    </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
    <cookie_mask>255</cookie_mask>
    <installHw>false</installHw>
    <priority>1</priority>
    <strict>false</strict>
    <table_id>0</table_id>
    <flow-name>FooXf8</flow-name>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>2048</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-destination>{}</ipv4-destination>
    </match>
</flow>"""
    final_body = raw_body.format(flow_id, out_port, dst_net)
    f = open("./flow/openflow{}:id_{}.xml".format(openflow_num, flow_id), "w")
    f.write(final_body)
    f.close()


def switch_xml_first(openflow_num, flow_id, dst_mac, dst_net, out_port):
    raw_body = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <barrier>false</barrier>
    <cookie>8</cookie>
    <id>{}</id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                    <dec-nw-ttl/>
                </action>
                <action>
                    <order>1</order>
                    <set-dl-dst-action>
                        <address>{}</address>
                    </set-dl-dst-action>
                </action>
                <action>
                    <order>2</order>
                    <output-action>
                        <output-node-connector>{}</output-node-connector>
                    </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
    <cookie_mask>255</cookie_mask>
    <installHw>false</installHw>
    <priority>1</priority>
    <strict>false</strict>
    <table_id>0</table_id>
    <flow-name>FooXf8</flow-name>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>2048</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-destination>{}</ipv4-destination>
    </match>
</flow>"""
    final_body = raw_body.format(flow_id, dst_mac, out_port, dst_net)
    f = open("./flow/openflow{}:id_{}.xml".format(openflow_num, flow_id), "w")
    f.write(final_body)
    f.close()


def Flow_Maker(NumOfNodes, Path_d, portList):
    for sw_index in range(NumOfNodes):
        flow_n = 1
        if sw_index + 1 in Path_d['send']:
            dst_mac_addr = '20:00:00:00:00:02'
            dst_net_addr = '10.0.2.1/32'
            for idx in range(len(Path_d['send'])):
                if Path_d['send'][idx] == sw_index + 1:
                    try:
                        outPort = portList[sw_index][Path_d['send'][idx + 1] - 1]
                        if idx == 0:
                            switch_xml_first(sw_index + 1, flow_n, dst_mac_addr, dst_net_addr, outPort)
                        else:
                            switch_xml(sw_index + 1, flow_n, dst_net_addr, outPort)

                        flow_n += 1
                    except:
                        switch_xml(sw_index + 1, flow_n, dst_net_addr, 1)
                        flow_n += 1
                    break
        if sw_index + 1 in Path_d['receive']:
            dst_mac_addr = '10:00:00:00:00:01'
            dst_net_addr = '10.0.1.1/32'
            for idx in range(len(Path_d['receive'])):
                if Path_d['receive'][idx] == sw_index + 1:
                    try:
                        outPort = portList[sw_index][Path_d['receive'][idx + 1] - 1]
                        if idx == 0:
                            switch_xml_first(sw_index + 1, flow_n, dst_mac_addr, dst_net_addr, outPort)
                        else:
                            switch_xml(sw_index + 1, flow_n, dst_net_addr, outPort)

                        flow_n += 1
                    except:
                        switch_xml(sw_index + 1, flow_n, dst_net_addr, 1)
                        flow_n += 1
                    break


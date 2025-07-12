def switch_xml(openflow_num,flow_id,dst_mac,out_port):
	raw_body="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
            <ethernet-destination>
                <address>{}</address>
            </ethernet-destination>
        </ethernet-match>
    </match>
</flow>"""
	final_body=raw_body.format(flow_id,out_port,dst_mac)
	f = open("./flow/openflow{}:id_{}.xml".format(openflow_num,flow_id),"w")
	f.write(final_body)
	f.close()

def router_xml(openflow_num,flow_id,dest_net,dest_mac,out_port):
    raw_body="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <strict>false</strict>
    <flow-name>FooXf102</flow-name>
    <id>{}</id>
    <table_id>0</table_id>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>2048</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-destination>{}</ipv4-destination>
    </match>
    <priority>2</priority>
    <installHw>false</installHw>
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
    
</flow>"""
    final_body=raw_body.format(flow_id,dest_net,dest_mac,out_port)
    f = open("./flow/openflow{}:id_{}.xml".format(openflow_num,flow_id),"w")
    f.write(final_body)
    f.close()



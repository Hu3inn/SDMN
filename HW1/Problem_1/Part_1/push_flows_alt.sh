#!/bin/bash

# this is doing the same flow management, it is just a more precise address for switches using ARP protocol
ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:02,actions=output:2
ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:01,actions=output:1

ovs-ofctl add-flow s2 dl_dst=00:00:00:00:00:01,actions=output:2
ovs-ofctl add-flow s2 dl_dst=00:00:00:00:00:02,actions=output:1

#the reason this two following lines are needed is that this mac addresses needs to be matched in ARP(Address resolution protocol) for handling the data packet
ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,actions=flood
ovs-ofctl add-flow s2 dl_type=0x806,nw_proto=1,actions=flood

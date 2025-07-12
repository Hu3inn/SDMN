#!/bin/bash

# Add flows to switches, this is a very simple handling, whatever (data packets) comes in one port, will go out from the other port. In more complex scenarios and topologies we need a protocol like ARP for handling packets
ovs-ofctl add-flow s1 "in_port=1,actions=output:2"
ovs-ofctl add-flow s1 "in_port=2,actions=output:1"

ovs-ofctl add-flow s2 "in_port=1,actions=output:2"
ovs-ofctl add-flow s2 "in_port=2,actions=output:1"




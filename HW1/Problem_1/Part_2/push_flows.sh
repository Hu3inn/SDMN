#!/bin/bash 

ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:03,actions=output:2 #destination mac : router
ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:01,actions=output:1 

ovs-ofctl add-flow s2 dl_dst=00:00:00:00:00:03,actions=output:2 #destination mac : router
ovs-ofctl add-flow s2 dl_dst=00:00:00:00:00:02,actions=output:1

ovs-ofctl add-flow s3 dl_type=0x0800,nw_dst=10.0.2.0/24,actions=mod_dl_dst:00:00:00:00:00:02,dec_ttl,output:2 
ovs-ofctl add-flow s3 dl_type=0x0800,nw_dst=10.0.1.0/24,actions=mod_dl_dst:00:00:00:00:00:01,dec_ttl,output:1 

#genuinely don't know what these below codes exactly do(it does have sth with ARP initial requests handling), it is combination ChatGPT, DeepSeek, Redit and etc.
ovs-ofctl add-flow s3 "dl_type=0x0806,nw_dst=10.0.2.0/24,actions=move:NXM_OF_ETH_SRC[]->NXM_OF_ETH_DST[],
mod_dl_src:00:00:00:00:00:03,
load:0x2->NXM_OF_ARP_OP[],
move:NXM_NX_ARP_SHA[]->NXM_NX_ARP_THA[],
move:NXM_OF_ARP_SPA[]->NXM_OF_ARP_TPA[],
load:0x000000000003->NXM_NX_ARP_SHA[],
load:0x0a000201->NXM_OF_ARP_SPA[],
in_port:2,output:1" 

ovs-ofctl add-flow s3 "dl_type=0x0806,nw_dst=10.0.1.0/24,actions=move:NXM_OF_ETH_SRC[]->NXM_OF_ETH_DST[],
mod_dl_src:00:00:00:00:00:03,
load:0x2->NXM_OF_ARP_OP[],
move:NXM_NX_ARP_SHA[]->NXM_NX_ARP_THA[],
move:NXM_OF_ARP_SPA[]->NXM_OF_ARP_TPA[],
load:0x000000000003->NXM_NX_ARP_SHA[],
load:0x0a000101->NXM_OF_ARP_SPA[],
in_port:1,output:2" 


ovs-ofctl add-flow s1 dl_type=0x0806,actions=flood  
ovs-ofctl add-flow s2 dl_type=0x0806,actions=flood 

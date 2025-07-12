#!/bin/bash

set -e

# Cleanup first (optional)
ip netns del node1 2>/dev/null || true
ip netns del node2 2>/dev/null || true
ip netns del node3 2>/dev/null || true
ip netns del node4 2>/dev/null || true
ip netns del router 2>/dev/null || true
ip link del br1 2>/dev/null || true
ip link del br2 2>/dev/null || true

# Create network namespaces
for ns in node1 node2 node3 node4 router; do
    ip netns add $ns
done

# Create bridges in root namespace
ip link add br1 type bridge
ip link set br1 up

ip link add br2 type bridge
ip link set br2 up

# Helper to create veth pairs
create_link() {
    ns=$1
    iface_ns=$2
    iface_br=$3
    bridge=$4

    ip link add $iface_br type veth peer name $iface_ns
    ip link set $iface_br master $bridge
    ip link set $iface_br up
    ip link set $iface_ns netns $ns
}

# Connect node1 and node2 to br1
create_link node1 veth_node1 veth_br1_node1 br1
create_link node2 veth_node2 veth_br1_node2 br1

# Connect node3 and node4 to br2
create_link node3 veth_node3 veth_br2_node3 br2
create_link node4 veth_node4 veth_br2_node4 br2

# Connect router to both br1 and br2
create_link router veth_r1 veth_br1_router br1
create_link router veth_r2 veth_br2_router br2

# Configure interfaces and IPs inside namespaces
ip netns exec node1 ip addr add 172.0.0.2/24 dev veth_node1
ip netns exec node2 ip addr add 172.0.0.3/24 dev veth_node2
ip netns exec node3 ip addr add 10.10.0.2/24 dev veth_node3
ip netns exec node4 ip addr add 10.10.0.3/24 dev veth_node4

ip netns exec router ip addr add 172.0.0.1/24 dev veth_r1
ip netns exec router ip addr add 10.10.0.1/24 dev veth_r2

# Bring up interfaces
for ns in node1 node2 node3 node4 router; do
    ip netns exec $ns ip link set lo up
    ip netns exec $ns ip link set veth_${ns} up || true
done

ip netns exec router ip link set veth_r1 up
ip netns exec router ip link set veth_r2 up

# Enable routing in router
ip netns exec router sysctl -w net.ipv4.ip_forward=1

# Add default routes in nodes
ip netns exec node1 ip route add default via 172.0.0.1
ip netns exec node2 ip route add default via 172.0.0.1
ip netns exec node3 ip route add default via 10.10.0.1
ip netns exec node4 ip route add default via 10.10.0.1

echo "✅ Topology created successfully!"


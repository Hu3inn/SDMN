###How to run Problem1


###1-implement the topology -->> run:
```
sudo ./create_topology
#or
sudo bash create_topology.sh
```

###2-getting ping -->> run:
```
sudo ./ping_nodes.sh $options $options
#or
sudo bash ./ping_nodes.sh $options $options
```
###$options=node1/node2/node3/node4/router/ip addresses


###3-cleaning up these hosts bridges and links:
```
sudo ./cleanup.sh
#or
sudo bash cleanup.sh
```



---



### Figure 2-Communication Without Router


In this topology, the router and its veth connections are removed. As a result, there is **no Layer 3 forwarding** between the two subnets:
- 172.0.0.0/24 (node1, node2)
- 10.10.0.0/24 (node3, node4)

By default, **hosts in different subnets cannot reach each other** unless there's a router or specific routing logic. To restore communication:

### Solution: Use Root Namespace as a Software Router

We can route between subnets using the root namespace as an L3 forwarder. Here's how:

### 1. Add veth pairs from `br1` and `br2` to root namespace:
- Keep existing `br1` and `br2` in the root namespace.
- Create two **veth pairs**, one end in each bridge and one end with IPs in the root namespace.

Example:

```
# Create links
ip link add root1 type veth peer name br1root
ip link add root2 type veth peer name br2root

# Attach one end to bridges
ip link set br1root master br1
ip link set br2root master br2
ip link set br1root up
ip link set br2root up

# Set up the other end (in root)
ip addr add 172.0.0.254/24 dev root1
ip addr add 10.10.0.254/24 dev root2
ip link set root1 up
ip link set root2 up
```

### 2. Enable IP forwarding on host

```
sysctl -w net.ipv4.ip_forward=1
```

### 3. Set default gateway for nodes

For node1 & node2: default gateway → 172.0.0.254
For node3 & node4: default gateway → 10.10.0.254

```
ip netns exec node1 ip route replace default via 172.0.0.254
ip netns exec node2 ip route replace default via 172.0.0.254
ip netns exec node3 ip route replace default via 10.10.0.254
ip netns exec node4 ip route replace default via 10.10.0.254
```




---




### Figure 3 – Multi-Host Namespace Networking solution

Now we distribute the topology:

- Server A: `node1`, `node2`, `br1`
- Server B: `node3`, `node4`, `br2`
- The two servers are **Layer 2-connected** (e.g., via a real or virtual switch)

There is **no router**, and bridges `br1` and `br2` are isolated. Inter-subnet routing is needed.

### Solution: Bridge Interconnection + Host Routing

We can simulate a router using **veth pairs and IP forwarding on each server**, plus use **VXLAN or GRE** to connect the bridges across servers.

### We can Use VXLAN to Interconnect Bridges 

### 1. Create VXLAN device on both servers

**Server A**:

```
ip link add vxlan0 type vxlan id 42 dev eth0 remote <ServerB-IP> dstport 4789
ip link set vxlan0 master br1
ip link set vxlan0 up
```

**Server B**:
```
ip link add vxlan0 type vxlan id 42 dev eth0 remote <ServerA-IP> dstport 4789
ip link set vxlan0 master br2
ip link set vxlan0 up
```

This makes br1 and br2 act like a single L2 broadcast domain across hosts.

### Add routing logic on both servers

Create veth pairs connected to each bridge and assign .254 addresses in root namespaces.
Enable ip_forward on both hosts.
Set the default gateway of nodes to those .254 addresses.

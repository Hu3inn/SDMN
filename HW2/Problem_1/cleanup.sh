#!/bin/bash

for ns in node1 node2 node3 node4 router; do
    ip netns del $ns 2>/dev/null && echo "Deleted namespace $ns"
done

for br in br1 br2; do
    ip link del $br 2>/dev/null && echo "Deleted bridge $br"
done

echo "✅ Cleanup complete."


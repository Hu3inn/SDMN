#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source-namespace-or-ip> <target-namespace-or-ip>"
    exit 1
fi

resolve_namespace() {
    input=$1
    # If it's a valid namespace name
    if ip netns list | grep -qw "$input"; then
        echo "$input"
        return
    fi

    # Otherwise, check if input is an IP assigned to a namespace
    for ns in $(ip netns list | cut -d' ' -f1); do
        if ip netns exec "$ns" ip -4 addr show | grep -q "$input"; then
            echo "$ns"
            return
        fi
    done

    echo ""
}

resolve_ip() {
    input=$1
    # If it's a valid IP (simple regex match)
    if [[ "$input" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "$input"
        return
    fi

    # Otherwise, treat as namespace and resolve IP inside
    if ! ip netns list | grep -qw "$input"; then
        echo ""
        return
    fi

    ip netns exec "$input" ip -4 addr show | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | head -n1
}

SOURCE_NS=$(resolve_namespace "$1")
TARGET_IP=$(resolve_ip "$2")

if [ -z "$SOURCE_NS" ]; then
    echo "❌ Could not resolve source namespace from: $1"
    exit 1
fi

if [ -z "$TARGET_IP" ]; then
    echo "❌ Could not resolve target IP from: $2"
    exit 1
fi

echo "🔁 Pinging $TARGET_IP from namespace $SOURCE_NS"
ip netns exec "$SOURCE_NS" ping -c 4 "$TARGET_IP"


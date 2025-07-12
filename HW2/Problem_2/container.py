#!/usr/bin/env python3
import os
import sys
import subprocess

def usage():
    print("Usage: ./container.py <hostname> [memory_limit_MB]")
    sys.exit(1)

def setup_cgroup(mem_limit_mb):
    cgroup_path = "/sys/fs/cgroup/memory/mycontainer"
    os.makedirs(cgroup_path, exist_ok=True)

    # Set memory limit
    with open(os.path.join(cgroup_path, "memory.limit_in_bytes"), "w") as f:
        f.write(str(mem_limit_mb * 1024 * 1024))

    # Add current process to cgroup
    with open(os.path.join(cgroup_path, "tasks"), "w") as f:
        f.write(str(os.getpid()))

def run_container(hostname, mem_limit_mb=None):
    if mem_limit_mb:
        setup_cgroup(mem_limit_mb)

    new_root = os.path.abspath("ubuntu-rootfs")

    # Command to run in child namespace
    command = [
        "unshare",
        "--mount",
        "--uts",
        "--net",
        "--pid",
        "--fork",
        "--mount-proc",
        "--user",
        "--map-root-user",
        "--",
        "/usr/bin/env", "-i",  # clean env
        "bash", "-c",
        f"""
        hostname {hostname} &&
        mount -t proc proc {new_root}/proc &&
        cd {new_root} &&
        mount --bind . . &&
        chroot . /bin/bash
        """
    ]

    subprocess.run(command)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    hostname = sys.argv[1]
    mem_limit_mb = int(sys.argv[2]) if len(sys.argv) == 3 else None
    run_container(hostname, mem_limit_mb)

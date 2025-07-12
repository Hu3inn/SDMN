### How to run this container

###1- Create root fliesystem directory and then extract ubuntu 20.04(ubuntu-rootfs): 

```
mkdir ubuntu-rootfs
#already made in the git repository
sudo sh -c 'docker export $(docker create ubuntu:20.04) | tar -C ubuntu-rootfs -xvf -'
```

It is worth mentionening that in this approach we get a very barebone, minimal ubuntu 20.04 image (Docker base layer), meaning that, theoratically, if you have ubuntu image (regardless how feature-rich it is, as long as it has the necessary root filesystems) can be extracted and put in this directory. But using Docker base layer image is a safe approach that involes 28 MB download and 75 MB storage when extracted.


### 2- Make sure cgroups are mounted (usually done automatically):

```
sudo mount -t cgroup -o memory none /sys/fs/cgroup/memory
```

### 3- Run the container

```
chmod +x container.py
#if it is not already executable

sudo ./container.py myhostname 100
# first argument is the name of the container, the second one is the amount of limited ram you desire in MB
```

Now you can use commands like `ls /` or `ps fax`.

Attention: the base layer image that docker provide doesn't come with iproute2, so in order to modify and mange network you need to do these steps to install iproute2:

```
sudo chroot ubuntu-rootfs /bin/bash

apt update
apt install iproute2 -y
exit

sudo ./container.py myhostname 100
#to rerun it so the new package get recognized
```

the reason behind this change root directory method instead of installing from the container cli is that the docker provided image doesn't come with package manager, so we use the host package manager in order to install a package

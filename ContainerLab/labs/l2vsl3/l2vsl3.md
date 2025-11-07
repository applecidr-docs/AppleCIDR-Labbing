---
title: Layer 2 vs. Layer 3 traffic
---
{% include clabnav.html %}
> During my time working in networking, I have come across plenty of people who have a hard time understanding the difference between layer 2 and layer 3 traffic. This lab attempts to explain the difference between the two, and why the distinction is important. 

# Lab topology
![l2vsl3 topology](/images/l2vsl3.png)
# Setup:
This lab will be using two Aruba CX switches and four Linux host machines. Two hosts are connected to each switch with one host on each switch configured for VLAN 10 and and one configured for VLAN 20.
## Create lab directory and clab.yml file
First, create a directory called 'l2vsl3' at the root of the home directory and cd into it:
```bash
mkdir ~/l2vsl3/ && cd ~/l2vsl3/
```
Create a clab yml file for the ContainerLab configuration using nano:
```bash
sudo nano l2vsl3.clab.yml
```

l2vsl2.clab.yml:
```yaml
name: l2vsl3

# Define the two Aruba CX switches and the four Linux hosts
topology:
  nodes:
    SwitchA:
      kind: aruba_aoscx
      image: aruba_aoscx:10_16_1006
    SwitchB:
      kind: aruba_aoscx
      image: aruba_aoscx:10_16_1006
    HostA:
      kind: generic_vm
      image: ubuntu:jammy
    HostB:
      kind: generic_vm
      image: ubuntu:jammy
    HostC:
      kind: generic_vm
      image: ubuntu:jammy
    HostD:
      kind: generic_vm
      image: ubuntu:jammy

# Define how the switches and hosts connect to one another
  links:
    - endpoints: [ SwitchA:1/1/1, SwitchB:1/1/1 ]
    - endpoints: [ SwitchA:1/1/3, HostA:eth1 ]
    - endpoints: [ SwitchA:1/1/4, HostB:eth1 ]
    - endpoints: [ SwitchB:1/1/3, HostC:eth1 ]
    - endpoints: [ SwitchB:1/1/4, HostD:eth1 ]
```

> Note, the image needs to match the docker image repository name and tag, which can be found by running `docker images`

Once the clab.yml file has been created, the lab needs deployed:
```bash
clab deploy
```

> Note, running `clab deploy` will only deploy the lab if you are in the lab directory (for this lab the ~/l2vsl3/ directory)


## Connect to Switches
Once the devices in the lab have booted (`clab inspect` will show the current status of each device), ssh into the two switches:
```bash
ssh admin@clab-l2vsl3-SwitchA
ssh admin@clab-l2vsl3-SwitchB
```

> Note, If your lab has a different name, the name of the devices will not be the same. Device names can be found by running `docker ps`. Names are listed under the NAMES column. Also, reading the /etc/hosts file will show the name of each device `cat /etc/hosts`

## Configure SwitchA
First, create VLAN 10 and VLAN 20 and name them:
```bash
SwitchA# conf t
SwitchA(config)# vlan 10
SwitchA(config-vlan-10)# name VLAN 10
SwitchA(config)# vlan 20
SwitchA(config-vlan-20)# name VLAN 20
```

Next, assign IP address to the VLAN 10 interface:
```bash
SwitchA(config)# interface vlan 10
SwitchA(config-if-vlan)# ip address 10.10.10.1/24
```

Next, configure interface 1/1/1:
```bash
SwitchA(config)# int 1/1/1
SwitchA(config-if)# no shut
SwitchA(config-if)# no routing
SwitchA(config-if)# vlan trunk allowed 10,20
```

Finally, configure the interfaces connected to HostA and HostB
```bash
SwitchA(config)# int 1/1/3
SwitchA(config-if)# no shut
SwitchA(config-if)# no routing
SwitchA(config-if)# vlan access 10
SwitchA(config)# int 1/1/4
SwitchA(config-if)# no shut
SwitchA(config-if)# no routing
SwitchA(config-if)# vlan access 20
```

## Configure SwitchB
SwitchB will have a very similar configuration:
```bash
SwitchB# conf t
SwitchB(config)# vlan 10
SwitchB(config-vlan-10)# name VLAN 10
SwitchB(config-vlan-10)# vlan 20
SwitchB(config-vlan-20)# name VLAN 20
SwitchB(config-vlan-20)# int vlan 20
SwitchB(config-if-vlan)# ip add 10.10.20.1/24
SwitchB(config-if-vlan)# int 1/1/1
SwitchB(config-if)# no shut
SwitchB(config-if)# no routing
SwitchB(config-if)# vlan trunk allowed 10,20
SwitchB(config-if)# int 1/1/3
SwitchB(config-if)# no shut
SwitchB(config-if)# no routing
SwitchB(config-if)# vlan access 10
SwitchB(config-if)# int 1/1/4
SwitchB(config-if)# no shut
SwitchB(config-if)# no routing
SwitchB(config-if)# vlan access 20
```

## Configure Hosts
SSH into each host:
```bash
ssh clab@clab-l2vsl3-HostA
ssh clab@clab-l2vsl3-HostB
ssh clab@clab-l2vsl3-HostC
ssh clab@clab-l2vsl3-HostD
```

> Note, the default username and password for the Ubuntu vm is 'clab' and 'clab@123'

## Assign IP addresses to each host
After SSH'ing into each host, assign the designated IP address to ens2
```bash
clab@HostA:~$ sudo ip addr add dev ens2 10.10.10.5/24
clab@HostA:~$ sudo ip link set dev ens2 up

clab@HostB:~$ sudo ip addr add dev ens2 10.10.20.5/24
clab@HostB:~$ sudo ip link set dev ens2 up

clab@HostC:~$ sudo ip addr add dev ens2 10.10.10.6/24
clab@HostC:~$ sudo ip link set dev ens2 up

clab@HostD:~$ sudo ip addr add dev ens2 10.10.20.6/24
clab@HostD:~$ sudo ip link set dev ens2 up
```

# Verify connectivity
Ping from HostA to HostC:
```bash
clab@HostA:~$ ping 10.10.10.6
PING 10.10.10.6 (10.10.10.6) 56(84) bytes of data.
64 bytes from 10.10.10.6: icmp_seq=1 ttl=64 time=1.88 ms
64 bytes from 10.10.10.6: icmp_seq=2 ttl=64 time=2.53 ms
64 bytes from 10.10.10.6: icmp_seq=3 ttl=64 time=2.57 ms
64 bytes from 10.10.10.6: icmp_seq=4 ttl=64 time=2.53 ms
--- 10.10.10.6 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.879/2.375/2.566/0.287 ms
```

HostA is able to ping HostC even though a default gateway has not been set on HostA.

Attempt to ping from HostA to HostB:
```bash
clab@HostA:~$ ping 10.10.20.5
PING 10.10.20.5 (10.10.20.5) 56(84) bytes of data.
^C
--- 10.10.20.5 ping statistics ---
9 packets transmitted, 0 received, 100% packet loss, time 8192ms
```

The ping fails. HostA is able to traverse both switches and communicate with HostC, but is not able to communicate with HostB on the same switch.

# Explaination
Pinging from HostA to HostC works because these hosts are in the same VLAN. VLANs are a layer 2 technology, so no routing is needed because ARP is providing HostA with HostC's MAC address. 

## Let's go through the ARP process
First, clear the ARP cache on HostA:
```bash
clab@HostA:~$ sudo ip neighbor flush all dev ens2
```

Next, ensure the ARP cache is clear:
```bash
clab@HostC:~$ sudo ip neighbor show dev ens2
```

Notice there are no ARP entries for dev ens2.

Find the MAC address of HostC:
```bash
clab@HostC:~$ ip addr show dev ens2
3: ens2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 0c:00:2b:11:82:01 brd ff:ff:ff:ff:ff:ff
    altname enp1s2
    inet 10.10.10.6/24 scope global ens2
       valid_lft forever preferred_lft forever
    inet6 fe80::e00:2bff:fe11:8201/64 scope link
       valid_lft forever preferred_lft forever
```

HostC's MAC address: 0c:00:2b:11:82:01

Now, ping from HostA to HostC to kick off the ARP process:
```bash
clab@HostA:~$ ping 10.10.10.6
PING 10.10.10.6 (10.10.10.6) 56(84) bytes of data.
64 bytes from 10.10.10.6: icmp_seq=1 ttl=64 time=1.88 ms
64 bytes from 10.10.10.6: icmp_seq=2 ttl=64 time=2.53 ms
64 bytes from 10.10.10.6: icmp_seq=3 ttl=64 time=2.57 ms
64 bytes from 10.10.10.6: icmp_seq=4 ttl=64 time=2.53 ms
--- 10.10.10.6 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.879/2.375/2.566/0.287 ms
```

### ARP
- 1. When pinging HostC, HostA will first check it's ARP cache for an entry for 10.10.10.6
- 2. Since the ARP cache of HostA has been flushed, HostA will send an ARP request 
# VLAN Basics

**VLANs (Virtual Local Area Networks)** are used to logically segment a network into smaller, isolated broadcast domains within the same physical infrastructure. By separating devices into VLANs, network administrators can control traffic flow, improve security, and reduce unnecessary broadcast traffic.

Instead of requiring separate physical switches for different network segments, VLANs allow multiple networks to coexist on the same hardware. Devices in different VLANs are logically separated and require routing to communicate with each other.

## Why VLANs Are Important

- **Improve security** by isolating sensitive systems and user groups  
- **Reduce broadcast traffic**, improving overall network performance  
- **Simplify network design** by logically grouping devices by function or role  
- **Increase flexibility** when moving devices without changing physical cabling  
- **Support scalable growth** as the network expands  

In short, VLANs provide a structured and efficient way to organize network traffic, making networks easier to manage, more secure, and better performing.

## Lab Overview

In this lab, we will be spinning up one switch and two end devices. First, we will create two new VLANs on the switch and move the devices into the separate VLANs to test connectivity, then we will move them into the same VLAN and do the same.

### I. Lab setup

This is a topographical view of what this lab will look like:

![vlans topology](/images/vlansTopo.png)

Personally, I like to create my labs within specific directories so that I can keep them all organized:

```bash
mkdir ~/Documents/vlans && cd ~/Documents/vlans
```

Inside the directory, I will create a new clab.yml file defining the devices in the lab:

> This lab will be utilizing the Aruba Switch Simulator and a generic Ubuntu VM. Instructions for downloading and installing these kinds can be found [here](https://github.com/srl-labs/vrnetlab/tree/master/ubuntu)

```bash
sudo nano vlans.clab.yml
```

```yaml
name: vlans

topology:
  nodes:
    # Specify an Aruba switch and two ubuntu VMs
    Switch01:
      kind: aruba_aoscx
      image: aruba_aoscx:10_16_1006
    HostA:
      kind: generic_vm
      image: ubuntu:jammy
    HostB:
      kind: generic_vm
      image: ubuntu:jammy

  # Specify the links between each VM and the Aruba switch
  # HostA will be connected to the Switch on interface 1/1/1 and HostB will be connect to interface 1/1/2
  links:
    - endpoints: ["Switch01:1/1/1", "HostA:eth1"]
    - endpoints: ["Switch01:1/1/2", "HostB:eth1"]

```

### II. Deploy the lab

Now that the lab is defined, we will deploy so that we can start labbing!

```bash
clab deploy
```
After a minute or two, the lab should be up and running. You can check the status by running either `docker ps` or `clab inspect`

### III. Configure the Switch

Once the lab has completed deploy, we will first SSH into the switch:

> The default username and password that are set are 'admin' and 'admin'

```bash
ssh admin@clab-vlans-Switch01
```
#### A. Create VLANs

```bash
Switch01# conf t
Switch01(config)# vlan 10
Switch01(config-vlan-10)# name Finance
Switch01(config-vlan-10)# vlan 11
Switch01(config-vlan-11)# name HR
```

#### B. Configure the switch interfaces

First, we will assign HostA to VLAN 10 and HostB to VLAN 11: 

> By default, the interface on the switch simulator are administratively shutdown and have routing enabled. 

```bash
Switch01(config)# int 1/1/1
Switch01(config-if)# no shut
Switch01(config-if)# no routing
Switch01(config-if)# vlan access 10
Switch01(config-if)# int 1/1/2
Switch01(config-if)# no shut
Switch01(config-if)# no routing
Switch01(config-if)# vlan access 11
Switch01(config-if)# wr me
```

### IV. Configure the Ubuntu VMs

Now, we will SSH into the VMs and assign IP addresses and enable the interface:

> The default username and password for the Ubuntu VMs are 'clab' and 'clab@123'

```bash
ssh clab@clab-vlans-HostA
```

```bash
clab@HostA:~$ sudo ip addr add dev ens2 192.168.0.1/24
clab@HostA:~$ sudo ip link set dev ens2 up
```

```bash
ssh clab@clab-vlans-HostB
```

```bash
clab@HostB:~$ sudo ip addr add dev ens2 192.168.0.2/24
clab@HostB:~$ sudo ip link set dev ens2 up
```

### V. Test Connectivity

Let's attempt to ping from HostA to HostV and visa vera:

```bash
clab@HostA:~$ ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
From 192.168.0.1 icmp_seq=1 Destination Host Unreachable
From 192.168.0.1 icmp_seq=2 Destination Host Unreachable
From 192.168.0.1 icmp_seq=3 Destination Host Unreachable
^C
--- 192.168.0.2 ping statistics ---
5 packets transmitted, 0 received, +3 errors, 100% packet loss, time 4097ms
```

```bash
clab@HostB:~$ ping 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
From 192.168.0.2 icmp_seq=1 Destination Host Unreachable
From 192.168.0.2 icmp_seq=2 Destination Host Unreachable
From 192.168.0.2 icmp_seq=3 Destination Host Unreachable
^C
--- 192.168.0.1 ping statistics ---
4 packets transmitted, 0 received, +3 errors, 100% packet loss, time 3058ms
```

The pings fail...

The devices are not within the same broadcast domain because each VLAN is a separate broadcast domain.

### VI. Move HostB into VLAN 10

Back on the switch, we will move interface 1/1/2 to VLAN 10:

```bash
Switch01# conf t
Switch01(config)# int 1/1/2
Switch01(config-if)# vlan access 10
Switch01(config-if)# wr me
Copying configuration: [Success]
```

### VII. Test Connectivity Again

Back to HostA again, let's see if we can ping HostB:

```bash
clab@HostA:~$ ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=64 time=2.37 ms
64 bytes from 192.168.0.2: icmp_seq=2 ttl=64 time=0.837 ms
64 bytes from 192.168.0.2: icmp_seq=3 ttl=64 time=2.03 ms
64 bytes from 192.168.0.2: icmp_seq=4 ttl=64 time=1.77 ms
^C
--- 192.168.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3015ms
rtt min/avg/max/mdev = 0.837/1.751/2.371/0.569 ms
```

Ping works!!! What about from HostB?

```bash
clab@HostB:~$ ping 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=64 time=2.42 ms
64 bytes from 192.168.0.1: icmp_seq=2 ttl=64 time=2.18 ms
64 bytes from 192.168.0.1: icmp_seq=3 ttl=64 time=1.94 ms
64 bytes from 192.168.0.1: icmp_seq=4 ttl=64 time=2.18 ms
^C
--- 192.168.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.937/2.180/2.419/0.170 ms
```

Yes! Full connectivity! 

Because the devices are now in the same VLAN (broadcast domain) they are able to communicate with each other.

##### Thanks for reading

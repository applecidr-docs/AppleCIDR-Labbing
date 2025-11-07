---
title: Layer 2 vs. Layer 3 traffic
---
{% include clabnav.html %}
> During my time working in networking, I have come across plenty of people who have a hard time understanding the difference between layer 2 and layer 3 traffic. This lab attempts to explain the difference between the two, and why the distinction is important. 

# I. Lab topology
![l2vsl3 topology](/images/l2vsl3.png)
# Setup:
This lab will be using two Aruba CX switches and four Linux host machines. Two hosts are connected to each switch with one host on each switch configured for VLAN 10 and and one configured for VLAN 20.
## A. Create lab directory and clab.yml file
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


## B. Connect to Switches
Once the devices in the lab have booted (`clab inspect` will show the current status of each device), ssh into the two switches:
```bash
ssh admin@clab-l2vsl3-SwitchA
ssh admin@clab-l2vsl3-SwitchB
```

> Note, If your lab has a different name, the name of the devices will not be the same. Device names can be found by running `docker ps`. Names are listed under the NAMES column. Also, reading the /etc/hosts file will show the name of each device `cat /etc/hosts`

## C. Configure SwitchA
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

## D. Configure SwitchB
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

## E. Configure Hosts
SSH into each host:
```bash
ssh clab@clab-l2vsl3-HostA
ssh clab@clab-l2vsl3-HostB
ssh clab@clab-l2vsl3-HostC
ssh clab@clab-l2vsl3-HostD
```

> Note, the default username and password for the Ubuntu vm is 'clab' and 'clab@123'

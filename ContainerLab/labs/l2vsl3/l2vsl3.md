---
title: Layer 2 vs. Layer 3 traffic
---
{% include clabnav.html %}

# Layer 2 vs. Layer 3 traffic

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

> Note, the image name in the yaml file needs to match the docker image repository name and tag, which can be found by running `docker images`

Once the .clab.yml file has been created, the lab needs deployed:
```bash
clab deploy
```

> Note, running `clab deploy` will only deploy the lab if you are in the lab directory (for this lab the ~/l2vsl3/ directory). Otherwise, you will need to specify the clab.yml file using the -t flag: `clab deploy -t ~/l2vsl3/l2vsl3.clab.yml`.


## Connect to Switches
Once the devices in the lab have booted (`clab inspect` will show the current status of each device), ssh into the two switches:
```bash
ssh admin@clab-l2vsl3-SwitchA
ssh admin@clab-l2vsl3-SwitchB
```

> Note, If your lab has a different name, the name of the devices will not be the same. Device names can be found by running `docker ps`. Names are listed under the NAMES column. Also, reading the /etc/hosts file will show the name of each device `cat /etc/hosts`.

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

> Note, the default username and password for the Ubuntu vm is 'clab' and 'clab@123'.

## Assign IP addresses to each host
After SSH'ing into each host, assign the designated IP address to ens2:
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
Pinging from HostA to HostC works because these hosts are in the same VLAN. VLANs are a layer 2 technology, so no routing is needed because ARP is providing HostA with HostC's MAC address (Layer 2 address). 

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
    link/ether 0c:00:9a:d6:d7:01 brd ff:ff:ff:ff:ff:ff
    altname enp1s2
    inet 10.10.10.6/24 scope global ens2
       valid_lft forever preferred_lft forever
    inet6 fe80::e00:2bff:fe11:8201/64 scope link
       valid_lft forever preferred_lft forever
```

HostC's MAC address in my lab: `0c:00:9a:d6:d7:01`

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

### ARP Process in Wireshark
Here is the initial ARP request coming from HostA:

![ARP Request](/images/arpRequest.png)
> Notice that the Source MAC address is HostA's MAC address and The Destination address is a broadcast address

HostC Then replys with it's MAC address:

![ARP Reply](/images/arpReply.png)
> HostC replies to HostA's ARP request by providing it's MAC address

Now that HostA has HostC's MAC address it sends a ping request:

![Ping Request](/images/pingRequest.png)
If we look at the details of the packet, we will see that the ping request has HostC's MAC address listed as the Layer 2 destination.
![Ping Request Detail](/images/pingRequestDetail.png)

Finally, HostC sends a ping reply to HostA to complete the ping process:

![Ping Reply](/images/pingReply.png)

This same process will not work if HostA attempts to ping HostB because when SwitchA recieves the ARP request from HostA it will not forward it out interface 1/1/4 (The interface HostB is connected to) because that interface is a member of VLAN 20, not VLAN 10. Because ARP is sending a broadcast at layer 2, the traffic will not leave the VLAN it originated from (VLAN 10).

# Routing
Now that we know each device can communicate with other devices within it's VLAN, let's add routing so that all of the devices can communicate. To do this, we will add a dedicated VLAN for Management. In order for the switches to be able to route, they both need an interface in the same vlan.

Let's add VLAN 100, give it a name of 'MGMT', assign an IP address according to the topology, and allow VLAN 100 to traverse the trunk between SwitchA and SwitchB:
```bash
SwitchA# conf t
SwitchA(config)# vlan 100
SwitchA(config-vlan-100)# name MGMT
SwitchA(config-vlan-100)# int vlan 100
SwitchA(config-if-vlan)# ip add 10.10.1.1/24
SwitchA(config-if-vlan)# int 1/1/1
SwitchA(config-if)# vlan trunk allowed 100

SwitchB# conf t
SwitchB(config)# vlan 100
SwitchB(config-vlan-100)# name MGMT
SwitchB(config-vlan-100)# int vlan 100
SwitchB(config-if-vlan)# ip add 10.10.1.2/24
SwitchB(config-if-vlan)# int 1/1/1
SwitchB(config-if)# vlan trunk allowed 100
```

Ensure connectivity between SwitchA and SwitchB via VLAN 100:
```bash
SwitchB(config)# ping 10.10.1.1
PING 10.10.1.1 (10.10.1.1) 100(128) bytes of data.
108 bytes from 10.10.1.1: icmp_seq=1 ttl=64 time=24.0 ms
108 bytes from 10.10.1.1: icmp_seq=2 ttl=64 time=2.50 ms
108 bytes from 10.10.1.1: icmp_seq=3 ttl=64 time=3.25 ms
108 bytes from 10.10.1.1: icmp_seq=4 ttl=64 time=2.99 ms
```

Now that the two switches have an IP address in the same subnet, we can use those IP addresses to create static routes. Let's start on SwitchA:
```bash
SwitchA# conf t
SwitchA(config)# ip route 10.10.20.0 255.255.255.0 10.10.1.2
```

> What this route statment is saying is "If you (SwitchA) recieve traffic with a destination address anywhere in the 10.10.20.0/24 subnet, forward that traffic to 10.10.1.2 (SwitchB).

With that route statment set, we now need a route statment set on SwitchB:
```bash
SwitchB# conf t
SwitchB(config)# ip route 10.10.10.0 255.255.255.0 10.10.1.1
```

> If this second route statement on SwitchB is not specified, traffic that is destinstined for 10.10.10.0/24 will not be able to reach it's destination. This includes return traffic that originated from that subnet (traffic from HostA or HostC for example).

SwitchA is now able to ping interface VLAN 20 on SwitchB and SwitchB can ping interface VLAN 10 on SwitchA:
```bash
SwitchA# ping 10.10.20.1
PING 10.10.20.1 (10.10.20.1) 100(128) bytes of data.
108 bytes from 10.10.20.1: icmp_seq=1 ttl=64 time=1.76 ms
108 bytes from 10.10.20.1: icmp_seq=2 ttl=64 time=3.44 ms
108 bytes from 10.10.20.1: icmp_seq=3 ttl=64 time=2.33 ms
108 bytes from 10.10.20.1: icmp_seq=4 ttl=64 time=1.25 ms

SwitchB# ping 10.10.10.1
PING 10.10.10.1 (10.10.10.1) 100(128) bytes of data.
108 bytes from 10.10.10.1: icmp_seq=1 ttl=64 time=1.13 ms
108 bytes from 10.10.10.1: icmp_seq=2 ttl=64 time=2.68 ms
108 bytes from 10.10.10.1: icmp_seq=3 ttl=64 time=2.33 ms
108 bytes from 10.10.10.1: icmp_seq=4 ttl=64 time=2.81 ms
```

But, if we attempt to ping from HostA to HostB, or HostD, or even interface VLAN 20 on SwitchB the ping continues to fail:
```bash
clab@HostA:~$ ping 10.10.20.5
PING 10.10.20.5 (10.10.20.5) 56(84) bytes of data.
^C
--- 10.10.20.5 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4076ms
```

This is because HostA needs to know where to send this traffic, and needs a default gateway in order to do so. 
> Typically, a default gateway would just be set on HostA using the following command `ip route add default dev ens2 via 10.10.10.1`. This would send all traffic to SwitchA for routing, but because we are utilizing vrnetlab to facilitate the Ubuntu VM, which essentially puts the Ubuntu VM inside of another VM. we will need to configure a route specifically to the 10.10.20.0/24 subnet:

```bash
clab@HostA:~$ sudo ip route add 10.10.20.0/24 via 10.10.10.1

clab@HostB:~$ sudo ip route add 10.10.10.0/24 via 10.10.20.1
```

> Now, HostA knows to send traffic destined for the subnet 10.10.20.0/24 to 10.10.10.1 (SwitchA), and HostB knows to send traffic destined for the subnet 10.10.10.0/24 to 10.10.20.1 (SwitchB). 

Ping from HostA to HostB: 
```bash
clab@HostA:~$ ping 10.10.20.5
PING 10.10.20.5 (10.10.20.5) 56(84) bytes of data.
64 bytes from 10.10.20.5: icmp_seq=1 ttl=64 time=1.88 ms
64 bytes from 10.10.20.5: icmp_seq=2 ttl=64 time=2.53 ms
64 bytes from 10.10.20.5: icmp_seq=3 ttl=64 time=2.57 ms
64 bytes from 10.10.20.5: icmp_seq=4 ttl=64 time=2.53 ms
--- 10.10.20.5 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.879/2.375/2.566/0.287 ms
```

Packets are now flowing from one VLAN to another thanks to routing!

# Conclusion
Two devices that are in the same broadcast domain (Layer 2 domain) can communicate with on another without the help of routing thanks to the ARP process. A switch will forward broadcast traffic along to any interface that's in the same broadcast domain (in the case of this lab VLAN 10) allowing the ARP process to run successfully, providing the destination machine's MAC address to the originating machine, which ultimatley allows that originating machine to send a successful ping request via MAC address. 

When we need to be able to traverse from one Layer 2 domain to another, Layer 3 needs to get involved. Layer 3 relys on IP addresses and routing in order to forward traffic. For this lab the switches are acting as both the Layer 2 and Layer 3 device (often referred to as multilayer switches) which gives them the ability to perform routing. 

Route statements are needed in order to tell the switches how to reach a subnet that is not locally connected. What route statements tell the switch is "if you receive traffic destined for this subnet, forward the traffic along to this IP address". Now, each switch knows how to reach subnets outside of the locally connected subnets and will forward the traffic along to a switch that does have said subnet locally connected. The final piece of the puzzle is providing a gateway to the hosts themselves. The gateway tells the host "If you are sending traffic to another device that's outside of your subnet, send that traffic to this IP address". One thing to keep in mind is the host's gateway has to be in the same subnet as the host itself, otherwise the traffic will never reach the gateway at Layer 2 in order for it to be routed further at Layer 3.

##### Thanks for reading!

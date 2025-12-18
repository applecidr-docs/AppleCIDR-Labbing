---
title: Quick Start
---
{% include clabnav.html %}
<br>
> Let's make a quick ContainerLab config file with two Aruba CX Switches connected to one another

# **Quick Start**
### I. Setup
#### A. Create a project directory
```bash
mkdir clab-quick-start && cd clab-quick-start
```
#### B. Create ContainerLab config file
ContainerLab uses yaml for configurtion. We will define the two switches as nodes and endpoints to connect the switches together. 
```bash
sudo nano aruba-quick-start.clab.yml
```
> The two switches will be called 'aos-SwitchA' and 'aos-SwitchB'. The two switches will be connect via interface 1/1/1.

```yaml
# Give the lab a name
name: aruba-quick-start

# Define the topology for the lab
topology:
  nodes:
    # Provide names for each node in the lab
    aos-SwitchA:
      # Kinds tell ContainerLab how to setup different devices when a lab is deployed
      kind: aruba_aoscx
      image: aruba_aos-cx:10_16_1006
    aos-SwitchB:
      kind: aruba_aoscx
      image: aruba_aos-cx:10_16_1006

  # Links tell ContainerLab how each device is going to connect to one another
  links:
    - endpoints: [aos-SwitchA:1/1/1, aos-SwitchB:1/1/1]
```
> If you'd like to find out more about the different Kinds that ContainerLab supports, please go to the official ContainerLab [Kinds](https://containerlab.dev/manual/kinds/) page.

#### C. Deploy the ContainerLab
We will run the clab deploy command from inside the aruba-quick-start directory. ContainerLab will read the .clab.yml file and deploy the lab.
> The Aruba CX Switch Simulator will take ~ 2 minutes to boot

```bash
clab deploy
```
#### D. Verify
ContainerLab will show the Name, Kind/Image, State, and IP address information for the lab as it is deployed. We can run `clab inspect` at anytime to see if the switches state has changed from 'starting' to 'healthy'. Once the lab has successfully deployed you can run the following to get further information about the containers:
```bash
docker ps
```
This docker command will show which docker containers are running and will also show you the name of the container.
> By default, ContainerLab will prepend 'clab' and the name of the lab to each node name. For instance, with this lab SwitchA's container will be named 'clab-aruba-quick-start-aos-SwitchA'

### II. Connecting to lab
#### A. SSH
As explained above, by using the `docker ps` command we can find the name of the Switches. The name can then be used to ssh into the switch as follows:
```bash
ssh admin@clab-aruba-quick-start-aos-SwitchA
```
> Two things happen when ContainerLab spins up a lab in regards to SSH. First, ContainerLab adds entries to the /etc/hosts file so that we can SSH into the devices by name. Then, ContainerLab add SSH configs for the nodes to the /etc/ssh/ssh_config.d directory so that we are not prompted to accept the SSH keys when we connect.

###### _Example of /etc/hosts file_
```bash
127.0.0.1       localhost

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
###### CLAB-aruba-quick-start-START ######
172.20.20.2     clab-aruba-quick-start-aos-SwitchA      # Kind: aruba_aoscx
172.20.20.3     clab-aruba-quick-start-aos-SwitchB      # Kind: aruba_aoscx
3fff:172:20:20::2       clab-aruba-quick-start-aos-SwitchA      # Kind: aruba_aoscx
3fff:172:20:20::3       clab-aruba-quick-start-aos-SwitchB      # Kind: aruba_aoscx
###### CLAB-aruba-quick-start-END ######
```

###### _Example of /etc/ssh/ssh_config.d/clab-aruba-quick-start.conf file_
```bash
# Containerlab SSH Config for the aruba-quick-start lab
Host clab-aruba-quick-start-aos-SwitchA
        User admin
        StrictHostKeyChecking=no
        UserKnownHostsFile=/dev/null

Host clab-aruba-quick-start-aos-SwitchB
        User admin
        StrictHostKeyChecking=no
        UserKnownHostsFile=/dev/null
```

Now that we have connected to the switch via SSH, we are being asked to provide a password for the admin user. During the creation of the Docker image, a python script is ran that sets the password of 'admin'. The script can be found within the vrnetlab directory. The full path is _/vrnetlab/aruba/aoscx/docker/launch.py_ and below is the code snippet that sets the password of 'admin' for the built-in admin user.
```python
# --- snip ---
if match:  # got a match!
  if ridx == 0:  # login
    self.logger.debug("trying to log in with 'admin'")
    self.wait_write("\r", wait=None)
    self.logger.debug("sent newline")
    self.wait_write("admin", wait="switch login:")
    self.logger.debug("sent username")
    self.wait_write("\r", wait="Password:")
    self.logger.debug("sent empty password")
    self.logger.debug("resetting password")
    self.wait_write("admin", wait="Enter new password:")
    self.wait_write("admin", wait="Confirm new password:")
# --- snip ---
```
### III. Run a show command
I have connected to the switches via the following SSH commands `ssh admin@clab-aruba-quick-start-aos-SwitchA` and `ssh admin@clab-aruba-quick-start-aos-SwitchB`. By default the interfaces of the switch simulator are administratively disabled, so before running our show commands we are going to enable the interfaces:
```shell
aos-SwitchA# conf t
aos-SwitchA(config)# int 1/1/1
aos-SwitchA(config-if)# no shut
aos-SwitchA(config-if)#

aos-SwitchB# conf t
aos-SwitchB(config)# int 1/1/1
aos-SwitchB(config-if)# no shut
aos-SwitchB(config-if)# 
```
Now that the interfaces have been enabled, we can run an LLDP neighbor command to see that the two switches are in fact connect to each other on interface 1/1/1
```shell
aos-SwitchA# show lldp neighbor-info 

LLDP Neighbor Information 
=========================

Total Neighbor Entries          : 1
Total Neighbor Entries Deleted  : 0
Total Neighbor Entries Dropped  : 0
Total Neighbor Entries Aged-Out : 0

LOCAL-PORT  CHASSIS-ID         PORT-ID                      PORT-DESC                    TTL      SYS-NAME    
-----------------------------------------------------------------------------------------------------------
1/1/1       08:00:09:b2:2c:3a  1/1/1                        1/1/1                        120      aos-SwitchB
```
```shell
aos-SwitchB# show lldp neighbor-info 

LLDP Neighbor Information 
=========================

Total Neighbor Entries          : 1
Total Neighbor Entries Deleted  : 0
Total Neighbor Entries Dropped  : 0
Total Neighbor Entries Aged-Out : 0

LOCAL-PORT  CHASSIS-ID         PORT-ID                      PORT-DESC                    TTL      SYS-NAME    
-----------------------------------------------------------------------------------------------------------
1/1/1       08:00:09:ea:bd:da  1/1/1                        1/1/1                        120      aos-SwitchA
```
### IV. Let's test Layer 3 connectivity!
We will assign an IP address to interface 1/1/1 on both switches and confirm connectivity using ping.
```shell
aos-SwitchA# conf t
aos-SwitchA(config)# int 1/1/1
aos-SwitchA(config-if)# ip address 10.10.10.1/24
```
```shell
aos-SwitchB# conf t
aos-SwitchB(config)# int 1/1/1
aos-SwitchB(config-if)# ip address 10.10.10.2/24
```
```shell
aos-SwitchB(config-if)# ping 10.10.10.1
PING 10.10.10.1 (10.10.10.1) 100(128) bytes of data.
108 bytes from 10.10.10.1: icmp_seq=1 ttl=64 time=16.0 ms
108 bytes from 10.10.10.1: icmp_seq=2 ttl=64 time=2.55 ms
108 bytes from 10.10.10.1: icmp_seq=3 ttl=64 time=3.09 ms
108 bytes from 10.10.10.1: icmp_seq=4 ttl=64 time=3.10 ms
108 bytes from 10.10.10.1: icmp_seq=5 ttl=64 time=3.10 ms

--- 10.10.10.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4003ms
rtt min/avg/max/mdev = 2.545/5.569/16.011/5.225 ms
```
### V. Finally, we will destroy the lab
Let's give the resources back to our host machine by destroying our lab
> It's important that the `clab` commands are ran in the context of our lab's directory. Specifically in this case, the destroy command must be ran inside the 'clab-quick-start' directory that was created at the beginning of this document.

```bash
clab destroy
```
ContainerLab will remove the docker containers, remove the /etc/hosts entries, and remove the SSH config files.
> This lab was completed entirely from the command line. If you prefer a more visual approach to labbing, you can install the VSCode ContainerLab Extension. Instructions for doing so and using the extension can be found [here](/ContainerLab/vscodeext).

##### Thanks for reading!

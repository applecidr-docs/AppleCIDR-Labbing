---
title: ContainerLab Quick Start
---
{% include nav.html %}
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
name: aruba-quick-start

topology:
  nodes:
    aos-SwitchA:
      kind: aruba_aoscx
      image: aruba_aos-cx:10_16_1006
    aos-SwitchB:
      kind: aruba_aoscx
      image: aruba_aos-cx:10_16_1006

  links:
    - endpoints: [aos-SwitchA:1/1/1, aos-SwitchB:1/1/1]
```
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
This docker command will show the docker containers are running and will also show you the name of the container.
> ContainerLab will prepend 'clab' and the name of the lab to each node name. For instance, with this lab SwitchA's container will be named 'clab-aruba-quick-start-aos-SwitchA'

### II. Connecting to lab
#### A. SSH
As explained above, by using the `docker ps` command we can find the name of the Switches. The name can then be used to ssh into the switch as follows:
```bash
ssh manager@clab-aruba-quick-start-aos-SwitchA
```
> Two things happen when ContainerLab spins up a lab in regards to SSH. First, ContainerLab adds entries to the /etc/hosts file so that we can SSH into the devices by name. Then, ContainerLab add SSH configs for the nodes to the /etc/ssh/ssh_config.d directory so that we are not prompted to accept the SSH keys when we connect.

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
###### _Example of /etc/hosts file_
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
###### _Example of /etc/ssh/ssh_config.d/clab-aruba-quick-start.conf file_

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
ContainerLab uses yaml for configurtion. We will define the two switches and endpoints to connect the switches together. 
> The configuration file
```yaml
name: aruba-quick-start

topology:
  nodes:
    aos-SwitchA:
      kind: aruba_aoscx
      image: aruba_aos-cx:10_16_1006
```

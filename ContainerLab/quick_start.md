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

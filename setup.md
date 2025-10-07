---
title: Prerequisites
---
{% include nav.html %}
<br>
> This setup was completed on Debian 12 (bookworm). Before installing Containerlab, we will need to ensure all prerequisites are met.

# **Prerequisites**
### I. User must have sudo privileges
```bash
sudo visudo
```
```bash
username ALL=(ALL:ALL) ALL
```
### II. Install Docker
⋅⋅⋅⋅* Uninstall any conflicting packages that may already be installed
```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

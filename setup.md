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
#### A. Uninstall any conflicting packages that may already be installed
```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```
#### B. Update APT packages, install ca-certificates and curl, and add Docker's official GPG key
```bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
#### C. Add the repository to APT sources and update to install
```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

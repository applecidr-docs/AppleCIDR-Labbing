---
title: Prerequisites
---
{% include clabnav.html %}
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
> The following instructions can be found on the official DockerDocs site <a href="https://docs.docker.com/engine/install/debian/">here</a>

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
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```bash
sudo apt-get update
```
#### D. Install the latest version of Docker packages
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
#### E. Verify that the Docker service started automatically, and if it did not, start it
```bash
sudo systemctl status docker
```
```bash
# In case the service did not start
sudo systemctl start docker
```
#### F. Verify that the installation was successful by running the hello-world image
```bash
sudo docker run hello-world
```
> This command downloads a test image, runs it in a container, and prints a confirmation message then exits.

### III. Download the Aruba CX Switch Simulator
> As of writing this, the newest version of the switch simulator is 10.16.1006 which will work with ContainerLab

#### A. If you do not already have an HPE Support Portal account you will need to create one <a href="https://networkingsupport.hpe.com/">here</a>
#### B. Once you are logged into the HPE Support Portal go to the Downloads page <a href="https://networkingsupport.hpe.com/globalsearch#tab=Software">here</a>, search for "Switch Simulator", and sort by "Date: New to Old"

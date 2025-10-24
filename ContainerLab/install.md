---
title: ContainerLab Install
---
{% include clabnav.html %}
<br>
> We will be adding the ContainerLab repository to the sources.list.d directory in order to install ContainerLab via APT. These instructions can be found in the official ContainerLab documentation <a href="https://containerlab.dev/install/#__tabbed_1_1">here</a>

# **Install**
### I. ContainerLab install
#### A. Add the ContainerLab repository to sources.list.d directory
```bash
echo "deb [trusted=yes] https://netdevops.fury.site/apt/ /" | \
sudo tee -a /etc/apt/sources.list.d/netdevops.list
```
#### B. Run APT update and install ContaierLab via APT
```bash
sudo apt update && sudo apt install containerlab
```
#### C. If you'd like to use the ContainerLab bash prompt (a little nicer and more functional than the default prompt), run the following script, then logout and log back in.
```bash
curl -sL https://containerlab.dev/setup | sudo -E bash -s "setup-bash-prompt"
```
### II. Install vrnetlab and configure the Aruba CX Switch Simulator
> Because the Aruba CX Switch Simulator is essentially a virtual machine, we will need to install vrnetlab to package the VM inside a container

#### A. Clone srl-labs/vrnetlab and cd into the vrnetlab directory
```bash
git clone https://github.com/srl-labs/vrnetlab && cd vrnetlab
```
#### B. cd into the aruba/aoscx directory 
```bash
cd aruba/aoscx
```
> At this point you can follow along with the README.md file in the aoscx directory, but I will also go through the steps here. The switch simulator zip file is in my Downloads directory, but you will need to substitute the file path to wherever you have the zip file saved to.

#### C. Extract VMDK file
Unzip the OVA file out of the zip file, untar the VMDK out of the OVA file, and copy the VMDK into the aoscx directory.
```bash
unzip ~/Downloads/AOS-CX_Switch_Simulator_10_16_1006_ova.zip ~/Downloads/AOS-CX_10_16_1006.ova
tar -xvf ~/Downloads/AOS-CX_10_16_1006.ova
cp ~/Downloads/arubaoscx-disk-image-genericx86-p4-20250822141147.vmdk arubaoscx-disk-image-genericx86-p4-20250822141147.vmdk
```
#### D. Run make command
Once the VMDK file is in the aoscx directory run the following command to make the docker image
```bash
make docker-image
```
#### E. Verify that the image is available
```bash
docker images
```
You should see vrnetlab/aruba_arubaos-cx listed as an available docker image
#### F. Tag the docker image (optional)
I am going to tag the docker image with the version of the image for ease of use. The existing tag may differ from the tag that you see below, but running `docker images` will show the image tag.
```bash
docker tag vrnetlab/vr-aoscx:20250822141147 aruba_aoscx:10_16_1006
```

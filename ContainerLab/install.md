---
title: ContainerLab Install
---
{% include nav.html %}
<br>
> We will be running the ContainerLab install script. These instructions can be found in the official ContainerLab documentation <a href="https://containerlab.dev/install/#__tabbed_1_1">here</a>

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
#### C. If you'd like to use the ContainerLab bash prompt (a little nicer and more functional than the default prompt), run the following script
```bash
curl -sL https://containerlab.dev/setup | sudo -E bash -s "setup-bash-prompt"
```

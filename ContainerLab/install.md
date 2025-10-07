---
title: ContainerLab Install
---
{% include nav.html %}
<br>
> We will be running the ContainerLab install script. These instructions can be found in the official ContainerLab documentation <a href="https://containerlab.dev/install/#__tabbed_1_1">here</a>

# **Install**
### I. ContainerLab install script
#### A. Download and install the latest release (this may require sudo)
```bash
bash -c "$(curl -sL https://get.containerlab.dev)"
```
#### B. If you'd like to use the ContainerLab bash prompt (a little nicer and more functional than the default prompt), run the following script
```bash
curl -sL https://containerlab.dev/setup | sudo -E bash -s "setup-bash-prompt"
```

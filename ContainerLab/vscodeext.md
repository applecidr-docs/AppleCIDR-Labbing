---
title: VS Code Extention
---
{% include clabnav.html %}
> If you're a visual learner, and you'd like a graphical way to interact with ContainerLab labs, you can install the VS Code Extension 'ContainerLab'

# I. Install VS Code
## A. Before installing the extension, you must install VS Code itself.
## B. If you are on Debian (as I am), you can run the following command to install VS Code via APT:

```bash
 sudo apt install code
```
## C. Now that VS Code is installed, open the program and click on the 'Extensions' icon in the menu on the left-hand side. The icon should look this this: 
## ![VS Code Extension icon](/images/vsCodeExt.png)
## D. Within the 'Extensions' menu search for 'ContainerLab' and click the blue 'Install' button
## E. Once installed, you can open clab.yml files within VS Code.

> For this example, I will be using quick-start.clab.yml

```bash
code quick-start.clab.yml
```

## F. Once your clab yml file is open in VS Code, you can the 'Graph' icon in the top right-hand corner of VS Code or use the keyboard shortcut `Ctrl+Alt+G`. This will open a new window in VS Code, showing a topographical representation of the lab.
## G. Now, you can add text, change icons, and ultimatly deploy the lab from within the topology viewer by clicking the 'play' button.
## H. Give the lab a couple of minutes to fully boot. The devices in the lab can now be interacted with directly. By right-clicking on a device you have the option to open an SSH console, a Shell console, view logs, and view properties.
## I. There is also an option run with WireShark packet capture on each device interface by right-clicking any of the links between devices and selecting one of the interfaces.
> The first time that you select an interface to run WireShark on, ContainerLab will download the ghostwire and packetflix containers. 

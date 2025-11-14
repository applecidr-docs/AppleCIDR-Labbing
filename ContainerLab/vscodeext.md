---
title: VS Code Extention
---
{% include clabnav.html %}
> If you're a visual learner, and you'd like a graphical way to interact with ContainerLab labs, you can install the VS Code Extension 'ContainerLab'

# Install VS Code
Before installing the extension, you must install VS Code itself. If you are on Debian (as I am), you can run the following command to install VS Code via APT:

```bash
 sudo apt install code
```
Now that VS Code is installed, open the program and click on the 'Extensions' icon in the menu on the left-hand side. The icon should look this this: 
![VS Code Extension icon](/images/vsCodeExt.png)

Within the 'Extensions' menu search for 'ContainerLab' and click the blue 'Install' button. Once installed, you can open clab.yml files within VS Code.

> For this example, I will be using quick-start.clab.yml

```bash
code quick-start.clab.yml
```

Once your clab yaml file is open in VS Code, you can click the 'Graph' icon in the top right-hand corner of VS Code or use the keyboard shortcut `Ctrl+Alt+G`. This will open a new window in VS Code, showing a topographical representation of the lab. Now, you can add text, change icons, and ultimatly deploy the lab from within the topology viewer by clicking the 'play' button.

Give the lab a couple of minutes to fully boot. The devices in the lab can now be interacted with inside of VS Code. By right-clicking on a device you have the option to open an SSH console, a Shell console, view logs, and view properties:

![VS Code SSH](/images/vscode_ssh.png)

There is also the option to run a WireShark packet capture on each device interface by right-clicking any of the links between devices and selecting one of the interfaces:

![VS Code Wireshark](/images/vscode_wireshark.png)
> The first time that you select an interface to capture packets on, ContainerLab will automatically download and start up the ghostwire and packetflix containers that are necessary for WireShark to run. 

## Conclusion

Personally, I am a visual learner so having a topology to look at while labbing is extremely helpful for understanding how a lab is configured. I highly recommend installing and using this extension!

<p align="center" style="font-family: 'Lucida Handwriting', cursive; font-size: 16px; color:#b5e853">
Thanks for reading!
</p>

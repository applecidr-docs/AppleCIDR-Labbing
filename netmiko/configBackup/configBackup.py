import os
import yaml
from netmiko import ConnectHandler
from dotenv import load_dotenv

# Load the .env file in order to pass Username and Password from environment variables
load_dotenv()

# Assign Username and Password environment variables to variables in the script
switchUsername = os.getenv("SWITCH_USERNAME")
switchPass = os.getenv("SWITCH_PASS")

# Open the inventory file where the device inventory is saved
with open("inventory.yml") as f:
    inventory = yaml.safe_load(f)

# Iterate over devices in inventory and connect
for name, device in inventory["devices"].items():
    device_params = {
        "host": device["host"],
        "device_type": device["device_type"],
        "username": switchUsername,
        "password": switchPass,
    }

    print(f"Connecting to {name} ({device['host']})...")
    # After connecting to the switch save the running config to a ftfp server and use the hostname of the switch as the name of the config file
    try:
        net_connect = ConnectHandler(**device_params)
        hostname = net_connect.send_command('show hostname')
        config_commands = [ 'copy running-config tftp://ftfp_server/' + hostname +' cli' ]
        output = net_connect.send_config_set(config_commands)
        print(output)
        net_connect.disconnect()
    except Exception as e:
        print(f"Failed to connect to {name}: {e}")

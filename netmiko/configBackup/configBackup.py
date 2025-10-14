import os
from netmiko import ConnectHandler
from dotenv import load_dotenv

load_dotenv()
switchPass = os.getenv("SWITCH_PASS")

switch1 = {
    'device_type': 'aruba_aoscx',
    'host':   'switchIP',
    'username': 'manager',
    'password': switchPass,
    'port' : 22,
}

net_connect = ConnectHandler(**switch1)

hostname = net_connect.send_command('show hostname')
config_commands = [ 'copy running-config tftp://tftpServer/' + hostname +' cli' ]

output = net_connect.send_config_set(config_commands)
print(output)

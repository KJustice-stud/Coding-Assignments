import os
from netmiko import ConnectHandler
from paramiko.ssh_exception import (AuthenticationException,
                                   SSHException)
from netmiko import NetMikoTimeoutException
from getpass import getpass

USERNAME = input("Please enter your SSH username: ")
PASS = getpass("Please enter your SSH password: ")

device = {
    'ip': '192.168.112.10',
    'username': USERNAME,
    'password': PASS,
    'device_type': 'cisco_ios'
}

try:
    c = ConnectHandler(**device)
except AuthenticationException:
    print(f"Authentication failed for device {device['ip']}")
    exit(1)
except SSHException:
    print(f"SSH Issue. Are you sure SSH is enabled on device {device['ip']}?")
    exit(2)
except NetMikoTimeoutException:
    print(f"Device {device['ip']} is not reachable or is powered down.")
    exit(3)

try:
    output = c.send_command('show run')
except Exception as e:
    print(f"An error occurred: {e}")
    exit(4)

try:
    with open('backup.conf', 'x') as f:
        f.write(output)
except Exception as e:
    print(f"An error occurred while creating the backup file: {e}")
    exit(5)


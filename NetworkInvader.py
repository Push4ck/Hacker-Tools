import subprocess
import sys
import platform
import re


def change_ip(interface="", new_ip="", subnet_mask="", gateway="", check=False):
    if not interface:
        interface = input("Enter the interface name: ")
    if not new_ip:
        new_ip = input("Enter the new IP address: ")
    if not subnet_mask:
        subnet_mask = input("Enter the subnet mask: ")
    if not gateway:
        gateway = input("Enter the default gateway: ")

    if not interface or not new_ip or not subnet_mask or not gateway:
        print("Error: interface, new_ip, subnet_mask and gateway are all required parameters")
        return 1

    if not isinstance(new_ip, str) or not isinstance(subnet_mask, str) or not isinstance(gateway, str):
        print("Error: Invalid input type. All inputs must be strings.")
        return 1

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", new_ip):
        print("Error: Invalid IP address format")
        return 1

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", subnet_mask):
        print("Error: Invalid subnet mask format")
        return 1

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", gateway):
        print("Error: Invalid gateway format")
        return 1

    command_list = []
    if platform.system() == 'Linux':
        command_list.extend([
            ['ifconfig', interface, 'down'],
            ['ifconfig', interface, 'inet', new_ip, 'netmask', subnet_mask],
            ['ifconfig', interface, 'up'],
            ['route', 'add', 'default', 'gw', gateway]
        ])
    else:
        print(f"Error: This code is only supported on Linux systems. Current operating system is {platform.system()}.")
        return 1

    for command in command_list:
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            print(f"Error: Command '{' '.join(command)}' failed with error code {e.returncode}")
            return e.returncode

    if check:
        if platform.system() == 'Linux':
            try:
                subprocess.check_output(['ip', '-4', 'address', 'show', interface])
            except subprocess.CalledProcessError as e:
                print(f"Error: Command 'ip -4 address show {interface}' failed with error code {e.returncode}")
                return e.returncode


if __name__ == '__main__':
    sys.exit(change_ip())

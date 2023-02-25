import subprocess
import re
import platform
import os
import socket


def get_os():
    return platform.system()


def is_root():
    return os.geteuid() == 0


def is_connected():
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


def get_nearby_devices():
    # Check if the user has root privileges
    if not is_root():
        print("You need to have root privileges to run this script.")
        return []

    # Check if the operating system is Linux
    if get_os() != "Linux":
        print("This script can only be run on Linux.")
        return []

    # Check if arp-scan is installed
    try:
        subprocess.check_output(["which", "arp-scan"])
    except subprocess.CalledProcessError:
        print("arp-scan is not installed. Please install it and try again.")
        return []

    # Run the arp-scan command with --localnet option and capture the output
    output = subprocess.check_output(["arp-scan", "--localnet"]).decode()

    # If the output is empty, return an empty list
    if not output:
        return []

    # Split the output into separate lines
    lines = output.split("\n")
    devices = []

    # Loop through each line
    for line in lines:
        parts = line.split()

        # Check if the line has 3 parts (IP address, MAC address, and hostname)
        if len(parts) == 3:
            ip_address = parts[0]
            mac_address = parts[1]
            hostname = parts[2]

            # Check if the IP address and MAC address match the expected format
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address) is not None and re.match(r"^[a-fA-F0-9:]{17}$", mac_address) is not None:
                devices.append({"ip_address": ip_address, "mac_address": mac_address, "hostname": hostname})
    return devices


# Check if the device is connected to a network
if not is_connected():
    print("You are not connected to a network. Please connect to a network and try again.")
else:
    # Get the nearby devices
    devices = get_nearby_devices()

    # Print the list of devices
    if devices:
        print("Nearby devices:")
        for device in devices:
            print(f"IP address: {device['ip_address']}, MAC address: {device['mac_address']}, Hostname: {device['hostname']}")
    else:
        print("No devices found.")

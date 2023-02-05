# Import required libraries
import subprocess
import re

# Function to get nearby devices using arp-scan
def get_nearby_devices():
    # Run the arp-scan command with --localnet option and capture the output
    output = subprocess.run(["arp-scan", "--localnet"], capture_output=True).stdout.decode()

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
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address) and re.match(r"^[a-fA-F0-9:]{17}$", mac_address):
                devices.append({"ip_address": ip_address, "mac_address": mac_address, "hostname": hostname})
    return devices

# Get the nearby devices
devices = get_nearby_devices()

# Print the list of devices
print(devices)

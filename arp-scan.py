import subprocess
import re

def get_nearby_devices():
    output = subprocess.run(["arp-scan", "--localnet"], capture_output=True).stdout.decode()
    if not output:
        return []
    lines = output.split("\n")
    devices = []
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            ip_address = parts[0]
            mac_address = parts[1]
            hostname = parts[2]
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address) and re.match(r"^[a-fA-F0-9:]{17}$", mac_address):
                devices.append({"ip_address": ip_address, "mac_address": mac_address, "hostname": hostname})
    return devices

devices = get_nearby_devices()
print(devices)

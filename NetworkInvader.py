import subprocess

def change_ip(interface, new_ip, subnet_mask, gateway):
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'inet', new_ip, 'netmask', subnet_mask])
    subprocess.call(['ifconfig', interface, 'up'])
    subprocess.call(['route', 'add', 'default', 'gw', gateway])

# Example usage
change_ip('eth0', '192.168.1.100', '255.255.255.0', '192.168.1.1')

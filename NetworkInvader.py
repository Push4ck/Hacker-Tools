import argparse
import sys
import re
import wmi


def validate_ip(ip: str) -> bool:
    """Check if the provided string is a valid IPv4 address."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split('.'))


def list_interfaces():
    """Print all active IP-enabled interfaces."""
    w = wmi.WMI()
    print("🔧 Available Network Interfaces:")
    for nic in w.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        print(f"  - {nic.Description}")


def change_ip(interface: str, new_ip: str, subnet: str, gateway: str) -> int:
    """Change IP address, subnet mask, and gateway of the given interface."""
    w = wmi.WMI()
    adapters = w.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    for nic in adapters:
        if nic.Description == interface:
            ip_result = nic.EnableStatic(IPAddress=[new_ip], SubnetMask=[subnet])
            gw_result = nic.SetGateways(DefaultIPGateway=[gateway])

            if ip_result[0] != 0:
                print(f"❌ Failed to set IP address. Error code: {ip_result[0]}")
                return ip_result[0]

            if gw_result[0] != 0:
                print(f"❌ Failed to set default gateway. Error code: {gw_result[0]}")
                return gw_result[0]

            print("✅ IP address and gateway configured successfully.")
            return 0

    print(f"❌ Interface '{interface}' not found.")
    return 1


def check_config(interface: str):
    """Display current IP config for the given interface."""
    w = wmi.WMI()
    for nic in w.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if nic.Description == interface:
            print("🔍 Current IP Configuration:")
            print(f"  Interface: {interface}")
            print(f"  IP Address: {nic.IPAddress[0]}")
            print(f"  Subnet Mask: {nic.IPSubnet[0]}")
            print(f"  Gateway: {nic.DefaultIPGateway[0]}")
            return
    print(f"⚠️ Interface '{interface}' not found.")


def main():
    parser = argparse.ArgumentParser(
        description="Set static IP, subnet mask, and gateway for a network interface on Windows.",
        epilog="Example: python change_ip.py --interface 'Intel(R) Ethernet Connection' --ip 192.168.1.100 --subnet 255.255.255.0 --gateway 192.168.1.1 --check"
    )

    parser.add_argument('--interface', help="Interface name (use --list to find one)")
    parser.add_argument('--ip', help="New IP address (e.g., 192.168.1.100)")
    parser.add_argument('--subnet', help="Subnet mask (e.g., 255.255.255.0)")
    parser.add_argument('--gateway', help="Default gateway (e.g., 192.168.1.1)")
    parser.add_argument('--check', action='store_true', help="Check and display new configuration")
    parser.add_argument('--list', action='store_true', help="List available network interfaces")

    args = parser.parse_args()

    if args.list:
        list_interfaces()
        sys.exit(0)

    if not all([args.interface, args.ip, args.subnet, args.gateway]):
        print("❌ Error: --interface, --ip, --subnet, and --gateway are required unless using --list.")
        parser.print_help()
        sys.exit(1)

    for label, val in [('IP', args.ip), ('Subnet', args.subnet), ('Gateway', args.gateway)]:
        if not validate_ip(val):
            print(f"❌ Invalid {label} format: {val}")
            sys.exit(1)

    exit_code = change_ip(args.interface, args.ip, args.subnet, args.gateway)

    if args.check:
        check_config(args.interface)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
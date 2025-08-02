#!/usr/bin/env python3
"""
NetBreach - Professional IP Configuration Tool
Fast and reliable network interface configuration for Windows systems.
"""

import argparse
import sys
import re
import os
import time
from typing import List, Dict, Optional, Tuple


# Check for WMI dependency
try:
    import wmi
except ImportError:
    print("❌ Error: WMI module not found. Install with: pip install WMI")
    sys.exit(1)


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Display the application banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ███╗   ██╗███████╗████████╗██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗
 ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║
 ██╔██╗ ██║█████╗     ██║   ██████╔╝██████╔╝█████╗  ███████║██║     ███████║
 ██║╚██╗██║██╔══╝     ██║   ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║
 ██║ ╚████║███████╗   ██║   ██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║
 ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BLUE}    Professional IP Configuration Tool v2.0{Colors.ENDC}
{Colors.CYAN}    Windows Network Interface Manager{Colors.ENDC}
    {'─' * 63}
"""
    print(banner)


def validate_ip(ip: str) -> bool:
    """
    Validate IPv4 address format
    
    Args:
        ip (str): IP address to validate
        
    Returns:
        bool: True if valid IPv4 address
    """
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    try:
        return all(0 <= int(part) <= 255 for part in ip.split('.'))
    except ValueError:
        return False


def validate_subnet_mask(subnet: str) -> bool:
    """
    Validate subnet mask format and values
    
    Args:
        subnet (str): Subnet mask to validate
        
    Returns:
        bool: True if valid subnet mask
    """
    if not validate_ip(subnet):
        return False
    
    # Common valid subnet masks
    valid_masks = [
        "255.255.255.255", "255.255.255.254", "255.255.255.252", "255.255.255.248",
        "255.255.255.240", "255.255.255.224", "255.255.255.192", "255.255.255.128",
        "255.255.255.0", "255.255.254.0", "255.255.252.0", "255.255.248.0",
        "255.255.240.0", "255.255.224.0", "255.255.192.0", "255.255.128.0",
        "255.255.0.0", "255.254.0.0", "255.252.0.0", "255.248.0.0",
        "255.240.0.0", "255.224.0.0", "255.192.0.0", "255.128.0.0",
        "255.0.0.0", "254.0.0.0", "252.0.0.0", "248.0.0.0",
        "240.0.0.0", "224.0.0.0", "192.0.0.0", "128.0.0.0"
    ]
    
    return subnet in valid_masks


def check_admin_privileges() -> bool:
    """Check if running with administrator privileges"""
    try:
        return os.access(sys.executable, os.W_OK) and os.access("C:\\Windows\\System32", os.W_OK)
    except:
        return False


def get_network_interfaces() -> List[Dict[str, str]]:
    """
    Get list of all IP-enabled network interfaces
    
    Returns:
        List[Dict[str, str]]: List of interface information
    """
    try:
        w = wmi.WMI()
        interfaces = []
        
        for nic in w.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            interface_info = {
                'description': nic.Description,
                'index': nic.Index,
                'ip_address': nic.IPAddress[0] if nic.IPAddress else 'N/A',
                'subnet_mask': nic.IPSubnet[0] if nic.IPSubnet else 'N/A',
                'gateway': nic.DefaultIPGateway[0] if nic.DefaultIPGateway else 'N/A',
                'dhcp_enabled': nic.DHCPEnabled,
                'mac_address': nic.MACAddress
            }
            interfaces.append(interface_info)
            
        return interfaces
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to retrieve network interfaces: {str(e)}")
        return []


def display_interfaces(verbose: bool = False):
    """Display all available network interfaces in a formatted table"""
    interfaces = get_network_interfaces()
    
    if not interfaces:
        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} No IP-enabled network interfaces found.")
        return
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}🔧 AVAILABLE NETWORK INTERFACES ({len(interfaces)} found){Colors.ENDC}")
    print("─" * 90)
    
    if verbose:
        print(f"{Colors.BOLD}{'#':<3} {'Interface Name':<35} {'IP Address':<15} {'DHCP':<5} {'Status':<8}{Colors.ENDC}")
        print("─" * 90)
        
        for i, interface in enumerate(interfaces, 1):
            dhcp_status = Colors.GREEN + "Yes" + Colors.ENDC if interface['dhcp_enabled'] else Colors.YELLOW + "No" + Colors.ENDC
            status = Colors.GREEN + "Active" + Colors.ENDC if interface['ip_address'] != 'N/A' else Colors.RED + "Inactive" + Colors.ENDC
            
            print(f"{Colors.CYAN}{i:<3}{Colors.ENDC} {interface['description'][:34]:<35} "
                  f"{interface['ip_address']:<15} {dhcp_status:<12} {status:<15}")
    else:
        for i, interface in enumerate(interfaces, 1):
            dhcp_indicator = f"{Colors.GREEN}[DHCP]{Colors.ENDC}" if interface['dhcp_enabled'] else f"{Colors.YELLOW}[Static]{Colors.ENDC}"
            print(f"{Colors.CYAN}{i:2}.{Colors.ENDC} {interface['description']} {dhcp_indicator}")
    
    print("─" * 90)


def display_interface_config(interface_name: str):
    """Display detailed configuration for a specific interface"""
    try:
        w = wmi.WMI()
        
        for nic in w.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if nic.Description == interface_name:
                print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 INTERFACE CONFIGURATION{Colors.ENDC}")
                print("─" * 50)
                print(f"{Colors.BOLD}Interface:{Colors.ENDC} {nic.Description}")
                print(f"{Colors.BOLD}MAC Address:{Colors.ENDC} {nic.MACAddress}")
                print(f"{Colors.BOLD}IP Address:{Colors.ENDC} {nic.IPAddress[0] if nic.IPAddress else 'N/A'}")
                print(f"{Colors.BOLD}Subnet Mask:{Colors.ENDC} {nic.IPSubnet[0] if nic.IPSubnet else 'N/A'}")
                print(f"{Colors.BOLD}Default Gateway:{Colors.ENDC} {nic.DefaultIPGateway[0] if nic.DefaultIPGateway else 'N/A'}")
                print(f"{Colors.BOLD}DHCP Enabled:{Colors.ENDC} {'Yes' if nic.DHCPEnabled else 'No'}")
                
                if nic.DNSServerSearchOrder:
                    print(f"{Colors.BOLD}DNS Servers:{Colors.ENDC}")
                    for dns in nic.DNSServerSearchOrder:
                        print(f"  • {dns}")
                
                print("─" * 50)
                return True
                
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Interface '{interface_name}' not found.")
        return False
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to retrieve interface configuration: {str(e)}")
        return False


def change_ip_configuration(interface_name: str, ip_address: str, subnet_mask: str, gateway: str, verbose: bool = False) -> int:
    """
    Change IP configuration for the specified interface
    
    Args:
        interface_name (str): Name of the network interface
        ip_address (str): New IP address
        subnet_mask (str): New subnet mask
        gateway (str): New default gateway
        verbose (bool): Enable verbose output
        
    Returns:
        int: 0 on success, error code on failure
    """
    try:
        if verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Configuring interface: {interface_name}")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} IP Address: {ip_address}")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Subnet Mask: {subnet_mask}")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Gateway: {gateway}")
            
        w = wmi.WMI()
        
        for nic in w.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if nic.Description == interface_name:
                if verbose:
                    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Found interface, applying configuration...")
                
                # Set static IP address and subnet mask
                ip_result = nic.EnableStatic(IPAddress=[ip_address], SubnetMask=[subnet_mask])
                
                if ip_result[0] != 0:
                    error_messages = {
                        1: "Successful completion, reboot required",
                        64: "Method not supported on this platform",
                        65: "Unknown failure",
                        66: "Invalid subnet mask",
                        67: "An error occurred while processing an Instance",
                        68: "Invalid input parameter",
                        69: "More than 5 gateways specified",
                        70: "Invalid IP address",
                        71: "Invalid gateway IP address",
                        91: "Access denied",
                        92: "Address not associated with an endpoint"
                    }
                    
                    error_msg = error_messages.get(ip_result[0], f"Unknown error code: {ip_result[0]}")
                    print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to set IP address: {error_msg}")
                    
                    if ip_result[0] == 1:
                        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Configuration applied but requires reboot to take effect.")
                        return 0
                    
                    return ip_result[0]
                
                # Set default gateway
                gw_result = nic.SetGateways(DefaultIPGateway=[gateway])
                
                if gw_result[0] != 0:
                    error_messages = {
                        1: "Successful completion, reboot required",
                        64: "Method not supported on this platform",
                        65: "Unknown failure",
                        66: "Invalid subnet mask",
                        67: "An error occurred while processing an Instance",
                        68: "Invalid input parameter",
                        69: "More than 5 gateways specified",
                        70: "Invalid IP address",
                        71: "Invalid gateway IP address",
                        91: "Access denied"
                    }
                    
                    error_msg = error_messages.get(gw_result[0], f"Unknown error code: {gw_result[0]}")
                    print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to set gateway: {error_msg}")
                    
                    if gw_result[0] == 1:
                        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Gateway configured but requires reboot to take effect.")
                        return 0
                    
                    return gw_result[0]
                
                print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} IP configuration applied successfully!")
                
                if verbose:
                    time.sleep(1)  # Give system time to apply changes
                    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Verifying configuration...")
                    display_interface_config(interface_name)
                
                return 0
                
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Interface '{interface_name}' not found.")
        return 1
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to change IP configuration: {str(e)}")
        return 1


def enable_dhcp(interface_name: str, verbose: bool = False) -> int:
    """
    Enable DHCP for the specified interface
    
    Args:
        interface_name (str): Name of the network interface
        verbose (bool): Enable verbose output
        
    Returns:
        int: 0 on success, error code on failure
    """
    try:
        if verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Enabling DHCP for interface: {interface_name}")
            
        w = wmi.WMI()
        
        for nic in w.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if nic.Description == interface_name:
                dhcp_result = nic.EnableDHCP()
                
                if dhcp_result[0] != 0:
                    print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to enable DHCP. Error code: {dhcp_result[0]}")
                    return dhcp_result[0]
                
                print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} DHCP enabled successfully!")
                return 0
                
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Interface '{interface_name}' not found.")
        return 1
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to enable DHCP: {str(e)}")
        return 1


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='NetBreach',
        description='Professional IP configuration tool for Windows network interfaces',
        epilog='''
Examples:
  %(prog)s --list                                    # List all network interfaces
  %(prog)s --list --verbose                          # Detailed interface information
  %(prog)s --check "Ethernet"                        # Show current config for interface
  %(prog)s --interface "Ethernet" --dhcp             # Enable DHCP
  %(prog)s --interface "Ethernet" --ip 192.168.1.100 --subnet 255.255.255.0 --gateway 192.168.1.1
  %(prog)s --interface "Wi-Fi" --ip 10.0.0.50 --subnet 255.255.255.0 --gateway 10.0.0.1 --verbose

Note: This tool requires administrator privileges to modify network settings.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--interface',
        metavar='NAME',
        help='Network interface name (use --list to find available interfaces)'
    )
    
    parser.add_argument(
        '--ip',
        metavar='ADDRESS',
        help='IP address to assign (e.g., 192.168.1.100)'
    )
    
    parser.add_argument(
        '--subnet',
        metavar='MASK',
        help='Subnet mask (e.g., 255.255.255.0)'
    )
    
    parser.add_argument(
        '--gateway',
        metavar='ADDRESS',
        help='Default gateway IP address (e.g., 192.168.1.1)'
    )
    
    parser.add_argument(
        '--dhcp',
        action='store_true',
        help='Enable DHCP for the specified interface'
    )
    
    parser.add_argument(
        '--check',
        metavar='INTERFACE',
        help='Display current configuration for the specified interface'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available network interfaces'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output with detailed information'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Suppress banner display'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0'
    )
    
    return parser


def main():
    """Main application entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Display banner unless suppressed
    if not args.no_banner:
        print_banner()
    
    # Check for administrator privileges
    if not check_admin_privileges():
        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Administrator privileges may be required for some operations.")
    
    # Handle list interfaces command
    if args.list:
        display_interfaces(args.verbose)
        sys.exit(0)
    
    # Handle check configuration command
    if args.check:
        if display_interface_config(args.check):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Handle DHCP enable command
    if args.dhcp:
        if not args.interface:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} --interface is required when using --dhcp")
            sys.exit(1)
        
        exit_code = enable_dhcp(args.interface, args.verbose)
        sys.exit(exit_code)
    
    # Handle static IP configuration
    if args.interface and args.ip and args.subnet and args.gateway:
        # Validate IP addresses
        validations = [
            ('IP address', args.ip, validate_ip),
            ('subnet mask', args.subnet, validate_subnet_mask),
            ('gateway', args.gateway, validate_ip)
        ]
        
        for name, value, validator in validations:
            if not validator(value):
                print(f"{Colors.RED}[ERROR]{Colors.ENDC} Invalid {name}: {value}")
                sys.exit(1)
        
        exit_code = change_ip_configuration(args.interface, args.ip, args.subnet, args.gateway, args.verbose)
        sys.exit(exit_code)
    
    # If no valid command combination provided
    if not any([args.list, args.check, args.dhcp, (args.interface and args.ip and args.subnet and args.gateway)]):
        print(f"{Colors.YELLOW}[INFO]{Colors.ENDC} No action specified. Use --help for available options.")
        parser.print_help()
        sys.exit(1)
    
    # Missing required arguments for static IP configuration
    if args.interface and not all([args.ip, args.subnet, args.gateway]):
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} For static IP configuration, --ip, --subnet, and --gateway are all required.")
        sys.exit(1)


if __name__ == '__main__':
    main()
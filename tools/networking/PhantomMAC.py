#!/usr/bin/env python3
"""
MacChanger Pro - Professional MAC Address Management Tool
Cross-platform MAC address modification for network testing and privacy.
"""

import subprocess
import argparse
import platform
import re
import sys
import os
import random
import time
import json
from pathlib import Path


# Color codes for cross-platform terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def disable_on_windows(cls):
        """Disable colors on Windows if not supported"""
        if os.name == 'nt':
            try:
                os.system('color')
            except:
                for attr in dir(cls):
                    if not attr.startswith('_') and attr != 'disable_on_windows':
                        setattr(cls, attr, '')


def print_banner():
    """Display the application banner with usage notice"""
    Colors.disable_on_windows()
    
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                     MacChanger Pro v2.0                     ║
║           Professional MAC Address Management Tool           ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.YELLOW}⚖️  RESPONSIBLE USE: This tool is for legitimate purposes only:
   • Network testing and troubleshooting
   • Privacy protection on public networks
   • Authorized penetration testing
   • Educational cybersecurity research{Colors.END}

{Colors.BLUE}🔧 Cross-platform MAC address modification (Windows/Linux/macOS)
🎲 Random MAC generation with vendor-specific options
📊 Interface discovery and MAC history tracking{Colors.END}
"""
    print(banner)


def check_privileges():
    """Check if the script is running with appropriate privileges"""
    system = platform.system()
    
    if system == "Windows":
        try:
            # Check if running as administrator
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print(f"{Colors.RED}❌ Administrator privileges required on Windows{Colors.END}")
                print(f"{Colors.YELLOW}💡 Please run as Administrator or use 'Run as administrator'{Colors.END}")
                return False
        except:
            print(f"{Colors.YELLOW}⚠️ Could not verify administrator privileges{Colors.END}")
    
    elif system in ["Linux", "Darwin"]:
        if os.geteuid() != 0:
            print(f"{Colors.RED}❌ Root privileges required on {system}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Please run with 'sudo' or as root user{Colors.END}")
            return False
    
    return True


def validate_mac_address(mac):
    """Validate MAC address format"""
    # Remove common separators and convert to lowercase
    mac = re.sub(r'[:-]', '', mac.lower())
    
    # Check if it's 12 hex characters
    if not re.match(r'^[0-9a-f]{12}$', mac):
        return None
    
    # Format as XX:XX:XX:XX:XX:XX
    formatted_mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
    return formatted_mac


def generate_random_mac(vendor_type="random"):
    """Generate a random MAC address with different vendor options"""
    
    # Common vendor prefixes for different types
    vendor_prefixes = {
        "cisco": ["00:1B:0D", "00:1C:0E", "00:1D:70", "00:21:55"],
        "intel": ["00:15:17", "00:16:76", "00:19:D1", "00:21:6A"],
        "dell": ["00:14:22", "00:15:C5", "00:19:B9", "00:21:70"],
        "hp": ["00:1F:29", "00:21:5A", "00:23:7D", "00:26:55"],
        "apple": ["00:16:CB", "00:17:F2", "00:19:E3", "00:1B:63"],
        "samsung": ["00:15:99", "00:16:32", "00:17:C9", "00:1A:8A"],
        "private": ["02", "06", "0A", "0E"],  # Locally administered
    }
    
    if vendor_type == "random":
        # Generate completely random MAC
        mac_bytes = [random.randint(0x00, 0xff) for _ in range(6)]
        # Set locally administered bit (bit 1 of first octet)
        mac_bytes[0] = (mac_bytes[0] & 0xfe) | 0x02
    elif vendor_type == "private":
        # Use private/locally administered prefix
        prefix = random.choice(vendor_prefixes["private"])
        mac_bytes = [int(prefix, 16)] + [random.randint(0x00, 0xff) for _ in range(5)]
    elif vendor_type in vendor_prefixes:
        # Use specific vendor prefix
        prefix = random.choice(vendor_prefixes[vendor_type])
        prefix_bytes = [int(x, 16) for x in prefix.split(':')]
        mac_bytes = prefix_bytes + [random.randint(0x00, 0xff) for _ in range(6 - len(prefix_bytes))]
    else:
        # Fallback to random
        mac_bytes = [random.randint(0x00, 0xff) for _ in range(6)]
        mac_bytes[0] = (mac_bytes[0] & 0xfe) | 0x02
    
    return ':'.join([f'{b:02x}' for b in mac_bytes])


def discover_interfaces():
    """Discover available network interfaces"""
    system = platform.system()
    interfaces = []
    
    try:
        if system == "Linux":
            # Use ip command or ifconfig
            try:
                output = subprocess.check_output(['ip', 'link', 'show'], text=True)
                for line in output.split('\n'):
                    match = re.search(r'\d+:\s+([^:]+):', line)
                    if match and match.group(1) != 'lo':
                        interfaces.append(match.group(1))
            except subprocess.CalledProcessError:
                # Fallback to ifconfig
                output = subprocess.check_output(['ifconfig'], text=True)
                interfaces = re.findall(r'^(\w+):', output, re.MULTILINE)
                interfaces = [i for i in interfaces if i != 'lo']
        
        elif system == "Darwin":  # macOS
            output = subprocess.check_output(['ifconfig'], text=True)
            interfaces = re.findall(r'^(\w+):', output, re.MULTILINE)
            interfaces = [i for i in interfaces if i not in ['lo0', 'gif0', 'stf0']]
        
        elif system == "Windows":
            # Method 1: Use Get-NetAdapter PowerShell command (most reliable)
            try:
                ps_command = 'Get-NetAdapter | Where-Object {$_.Status -eq "Up" -or $_.Status -eq "Disconnected"} | Select-Object -ExpandProperty Name'
                output = subprocess.check_output(['powershell', '-Command', ps_command], text=True)
                for line in output.split('\n'):
                    interface_name = line.strip()
                    if interface_name and 'Loopback' not in interface_name:
                        interfaces.append(interface_name)
            except subprocess.CalledProcessError:
                # Method 2: Fallback to netsh
                try:
                    output = subprocess.check_output(['netsh', 'interface', 'show', 'interface'], text=True)
                    for line in output.split('\n'):
                        if ('Connected' in line or 'Disconnected' in line) and 'Dedicated' in line:
                            parts = line.strip().split()
                            if len(parts) >= 4:
                                interface_name = ' '.join(parts[3:])
                                if interface_name and 'Loopback' not in interface_name:
                                    interfaces.append(interface_name)
                except subprocess.CalledProcessError:
                    # Method 3: Use wmic as last resort
                    try:
                        output = subprocess.check_output([
                            'wmic', 'networkadapter', 'where', 'NetConnectionID!=NULL', 
                            'get', 'NetConnectionID', '/format:csv'
                        ], text=True)
                        for line in output.split('\n'):
                            if line.strip() and 'NetConnectionID' not in line:
                                parts = line.strip().split(',')
                                if len(parts) >= 2 and parts[-1].strip():
                                    interface_name = parts[-1].strip()
                                    if 'Loopback' not in interface_name:
                                        interfaces.append(interface_name)
                    except subprocess.CalledProcessError:
                        pass
    
    except subprocess.CalledProcessError:
        pass
    
    return list(set(interfaces))  # Remove duplicates


def get_current_mac(interface):
    """Get current MAC address of specified interface"""
    system = platform.system()
    
    try:
        if system == "Linux":
            # Try ip command first
            try:
                output = subprocess.check_output(['ip', 'link', 'show', interface], text=True)
                match = re.search(r'link/ether\s+([0-9a-f:]{17})', output)
                if match:
                    return match.group(1)
            except subprocess.CalledProcessError:
                pass
            
            # Fallback to ifconfig
            output = subprocess.check_output(['ifconfig', interface], text=True)
            match = re.search(r'(?:ether|HWaddr)\s+([0-9a-f:]{17})', output, re.IGNORECASE)
            return match.group(1) if match else None
            
        elif system == "Darwin":  # macOS
            output = subprocess.check_output(['ifconfig', interface], text=True)
            match = re.search(r'ether\s+([0-9a-f:]{17})', output)
            return match.group(1) if match else None
            
        elif system == "Windows":
            # Method 1: Use wmic command for better interface matching
            try:
                # Get adapter configuration
                output = subprocess.check_output([
                    'wmic', 'networkadapter', 'where', f'NetConnectionID="{interface}"', 
                    'get', 'MACAddress', '/format:csv'
                ], text=True)
                
                for line in output.split('\n'):
                    if line.strip() and 'MACAddress' not in line and len(line.strip()) > 10:
                        parts = line.strip().split(',')
                        if len(parts) >= 2 and parts[-1].strip():
                            mac = parts[-1].strip()
                            if ':' not in mac and len(mac) == 12:
                                # Format MAC with colons
                                mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)]).lower()
                            return mac.lower()
            except subprocess.CalledProcessError:
                pass
            
            # Method 2: Use getmac command with better parsing
            try:
                output = subprocess.check_output(['getmac', '/fo', 'csv', '/v'], text=True)
                lines = output.split('\n')
                
                for i, line in enumerate(lines):
                    if interface.lower() in line.lower() and 'Physical Address' not in line:
                        # Look for MAC address pattern in this line
                        mac_match = re.search(r'([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})', line, re.IGNORECASE)
                        if mac_match:
                            mac = mac_match.group(1).replace('-', ':').lower()
                            return mac
            except subprocess.CalledProcessError:
                pass
            
            # Method 3: Use PowerShell as fallback
            try:
                ps_command = f'Get-NetAdapter -Name "{interface}" | Select-Object -ExpandProperty MacAddress'
                output = subprocess.check_output(['powershell', '-Command', ps_command], text=True)
                mac = output.strip()
                if mac and len(mac) >= 12:
                    # Convert to standard format
                    mac = mac.replace('-', ':').lower()
                    return mac
            except subprocess.CalledProcessError:
                pass
    
    except subprocess.CalledProcessError:
        pass
    
    return None


def change_mac_linux(interface, new_mac):
    """Change MAC address on Linux"""
    try:
        # Bring interface down
        subprocess.run(['ip', 'link', 'set', interface, 'down'], check=True)
        
        # Change MAC address
        subprocess.run(['ip', 'link', 'set', interface, 'address', new_mac], check=True)
        
        # Bring interface up
        subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
        
        return True
    except subprocess.CalledProcessError:
        # Fallback to ifconfig
        try:
            subprocess.run(['ifconfig', interface, 'down'], check=True)
            subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac], check=True)
            subprocess.run(['ifconfig', interface, 'up'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False


def change_mac_macos(interface, new_mac):
    """Change MAC address on macOS"""
    try:
        subprocess.run(['sudo', 'ifconfig', interface, 'ether', new_mac], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def change_mac_windows(interface, new_mac):
    """Change MAC address on Windows"""
    try:
        # Remove colons and convert to uppercase
        clean_mac = new_mac.replace(':', '').upper()
        
        # Disable interface
        subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{interface}"', 'admin=disable'], 
                      check=True, capture_output=True)
        
        # Find the registry key for the interface
        reg_output = subprocess.check_output([
            'reg', 'query', 
            r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}',
            '/s', '/f', interface
        ], text=True)
        
        # Extract registry key path
        reg_match = re.search(r'(HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\'
                             r'{4D36E972-E325-11CE-BFC1-08002BE10318}\\[0-9]+)', reg_output)
        
        if reg_match:
            reg_path = reg_match.group(1)
            
            # Set MAC address in registry
            subprocess.run([
                'reg', 'add', reg_path,
                '/v', 'NetworkAddress', '/t', 'REG_SZ', '/d', clean_mac, '/f'
            ], check=True, capture_output=True)
        
        # Enable interface
        subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{interface}"', 'admin=enable'], 
                      check=True, capture_output=True)
        
        # Wait for interface to come up
        time.sleep(3)
        
        return True
    except subprocess.CalledProcessError:
        return False


def restore_original_mac(interface):
    """Restore original MAC address"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Remove custom MAC from registry
            reg_output = subprocess.check_output([
                'reg', 'query', 
                r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}',
                '/s', '/f', interface
            ], text=True)
            
            reg_match = re.search(r'(HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\'
                                 r'{4D36E972-E325-11CE-BFC1-08002BE10318}\\[0-9]+)', reg_output)
            
            if reg_match:
                reg_path = reg_match.group(1)
                subprocess.run(['reg', 'delete', reg_path, '/v', 'NetworkAddress', '/f'], 
                              check=True, capture_output=True)
                
                # Restart interface
                subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{interface}"', 'admin=disable'], 
                              check=True, capture_output=True)
                subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{interface}"', 'admin=enable'], 
                              check=True, capture_output=True)
                return True
        
        else:
            # For Linux/macOS, restart network service or interface
            if system == "Linux":
                subprocess.run(['ip', 'link', 'set', interface, 'down'], check=True)
                subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
            elif system == "Darwin":
                subprocess.run(['ifconfig', interface, 'down'], check=True)
                subprocess.run(['ifconfig', interface, 'up'], check=True)
            return True
            
    except subprocess.CalledProcessError:
        return False


def save_mac_history(interface, old_mac, new_mac):
    """Save MAC change history to file"""
    history_file = Path.home() / '.macchanger_history.json'
    
    try:
        # Load existing history
        history = []
        if history_file.exists():
            with open(history_file, 'r') as f:
                history = json.load(f)
        
        # Add new entry
        entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'interface': interface,
            'old_mac': old_mac,
            'new_mac': new_mac,
            'system': platform.system()
        }
        history.append(entry)
        
        # Keep only last 100 entries
        history = history[-100:]
        
        # Save history
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception:
        pass  # Fail silently if can't save history


def display_interface_info():
    """Display available interfaces and their current MAC addresses"""
    interfaces = discover_interfaces()
    
    if not interfaces:
        print(f"{Colors.YELLOW}⚠️ No network interfaces found{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}🔍 Available Network Interfaces:{Colors.END}")
    print(f"{Colors.BOLD}{'─' * 50}{Colors.END}")
    
    for interface in interfaces:
        current_mac = get_current_mac(interface)
        mac_display = current_mac if current_mac else "Unknown"
        status_color = Colors.GREEN if current_mac else Colors.RED
        
        print(f"{Colors.CYAN}Interface:{Colors.END} {interface:<15} "
              f"{Colors.CYAN}MAC:{Colors.END} {status_color}{mac_display}{Colors.END}")


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog='macchanger-pro',
        description='🔧 MacChanger Pro - Professional MAC Address Management',
        epilog=f"""
{Colors.BOLD}Basic Usage:{Colors.END}
  {Colors.CYAN}macchanger-pro -i eth0 -m 02:11:22:33:44:55{Colors.END}
  {Colors.CYAN}macchanger-pro -i "Wi-Fi" --random{Colors.END}
  {Colors.CYAN}macchanger-pro --list{Colors.END}

{Colors.BOLD}Advanced Usage:{Colors.END}
  {Colors.CYAN}macchanger-pro -i eth0 --random --vendor cisco{Colors.END}
  {Colors.CYAN}macchanger-pro -i eth0 --restore{Colors.END}
  {Colors.CYAN}macchanger-pro -i wlan0 --random --vendor private{Colors.END}

{Colors.BOLD}Vendor Options:{Colors.END} cisco, intel, dell, hp, apple, samsung, private, random

{Colors.YELLOW}⚠️  Remember: Run with appropriate privileges (sudo/Administrator){Colors.END}
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Interface selection
    parser.add_argument(
        '-i', '--interface',
        help='Network interface name (e.g., eth0, Wi-Fi, wlan0)'
    )
    
    # MAC address options
    mac_group = parser.add_mutually_exclusive_group()
    mac_group.add_argument(
        '-m', '--mac',
        help='Specific MAC address to set (XX:XX:XX:XX:XX:XX format)'
    )
    mac_group.add_argument(
        '--random',
        action='store_true',
        help='Generate and set a random MAC address'
    )
    mac_group.add_argument(
        '--restore',
        action='store_true',
        help='Restore original MAC address'
    )
    
    # Vendor options for random MAC
    parser.add_argument(
        '--vendor',
        choices=['cisco', 'intel', 'dell', 'hp', 'apple', 'samsung', 'private', 'random'],
        default='private',
        help='Vendor type for random MAC generation (default: private)'
    )
    
    # Information display
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available network interfaces and their MAC addresses'
    )
    
    parser.add_argument(
        '--current',
        action='store_true',
        help='Show current MAC address of specified interface'
    )
    
    parser.add_argument(
        '--history',
        action='store_true',
        help='Show MAC change history'
    )
    
    # Output options
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress banner and minimize output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'{Colors.CYAN}MacChanger Pro v2.0{Colors.END} - Professional MAC Address Management'
    )
    
    return parser


def show_history():
    """Display MAC change history"""
    history_file = Path.home() / '.macchanger_history.json'
    
    if not history_file.exists():
        print(f"{Colors.YELLOW}📝 No MAC change history found{Colors.END}")
        return
    
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        if not history:
            print(f"{Colors.YELLOW}📝 MAC change history is empty{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}📝 MAC Change History (Last {len(history)} entries):{Colors.END}")
        print(f"{Colors.BOLD}{'─' * 80}{Colors.END}")
        
        for entry in history[-20:]:  # Show last 20 entries
            print(f"{Colors.CYAN}{entry['timestamp']}{Colors.END} | "
                  f"{Colors.YELLOW}{entry['interface']}{Colors.END} | "
                  f"{Colors.RED}{entry['old_mac']}{Colors.END} → "
                  f"{Colors.GREEN}{entry['new_mac']}{Colors.END} | "
                  f"{entry['system']}")
    
    except Exception as e:
        print(f"{Colors.RED}❌ Error reading history: {e}{Colors.END}")


def main():
    """Main application entry point"""
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        # Display banner unless in quiet mode
        if not args.quiet:
            print_banner()
        
        # Check for list interfaces option
        if args.list:
            display_interface_info()
            return
        
        # Check for history option
        if args.history:
            show_history()
            return
        
        # Validate interface is provided for other operations
        if not args.interface:
            print(f"{Colors.RED}❌ Interface must be specified with -i/--interface{Colors.END}")
            print(f"{Colors.YELLOW}💡 Use --list to see available interfaces{Colors.END}")
            sys.exit(1)
        
        # Check privileges
        if not check_privileges():
            sys.exit(1)
        
        interface = args.interface
        system = platform.system()
        
        # Get current MAC address
        current_mac = get_current_mac(interface)
        if not current_mac:
            print(f"{Colors.RED}❌ Could not retrieve MAC address for interface: {interface}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Use --list to see available interfaces{Colors.END}")
            sys.exit(1)
        
        # Show current MAC if requested
        if args.current:
            print(f"{Colors.CYAN}Interface:{Colors.END} {interface}")
            print(f"{Colors.CYAN}Current MAC:{Colors.END} {Colors.GREEN}{current_mac}{Colors.END}")
            return
        
        print(f"{Colors.CYAN}🖥️ Operating System:{Colors.END} {system}")
        print(f"{Colors.CYAN}🔌 Interface:{Colors.END} {interface}")
        print(f"{Colors.CYAN}📍 Current MAC:{Colors.END} {Colors.YELLOW}{current_mac}{Colors.END}")
        
        # Determine new MAC address
        new_mac = None
        
        if args.restore:
            print(f"{Colors.BLUE}🔄 Restoring original MAC address...{Colors.END}")
            success = restore_original_mac(interface)
            if success:
                restored_mac = get_current_mac(interface)
                print(f"{Colors.GREEN}✅ MAC address restored to: {restored_mac}{Colors.END}")
                save_mac_history(interface, current_mac, restored_mac)
            else:
                print(f"{Colors.RED}❌ Failed to restore original MAC address{Colors.END}")
            return
        
        elif args.random:
            new_mac = generate_random_mac(args.vendor)
            print(f"{Colors.BLUE}🎲 Generated random MAC:{Colors.END} {Colors.CYAN}{new_mac}{Colors.END} "
                  f"({args.vendor} vendor)")
        
        elif args.mac:
            new_mac = validate_mac_address(args.mac)
            if not new_mac:
                print(f"{Colors.RED}❌ Invalid MAC address format: {args.mac}{Colors.END}")
                print(f"{Colors.YELLOW}💡 Use format: XX:XX:XX:XX:XX:XX{Colors.END}")
                sys.exit(1)
        
        else:
            print(f"{Colors.RED}❌ No MAC address specified{Colors.END}")
            print(f"{Colors.YELLOW}💡 Use -m/--mac, --random, or --restore{Colors.END}")
            sys.exit(1)
        
        # Apply MAC address change
        if new_mac:
            print(f"{Colors.BLUE}🔧 Changing MAC address to: {new_mac}{Colors.END}")
            
            success = False
            if system == "Linux":
                success = change_mac_linux(interface, new_mac)
            elif system == "Darwin":
                success = change_mac_macos(interface, new_mac)
            elif system == "Windows":
                success = change_mac_windows(interface, new_mac)
            
            # Verify the change
            time.sleep(2)  # Wait for change to take effect
            final_mac = get_current_mac(interface)
            
            if success and final_mac and final_mac.lower() == new_mac.lower():
                print(f"{Colors.GREEN}✅ MAC address successfully changed!{Colors.END}")
                print(f"{Colors.CYAN}🎯 New MAC:{Colors.END} {Colors.GREEN}{final_mac}{Colors.END}")
                save_mac_history(interface, current_mac, final_mac)
            else:
                print(f"{Colors.RED}❌ MAC address change failed{Colors.END}")
                if final_mac:
                    print(f"{Colors.YELLOW}📍 Current MAC:{Colors.END} {final_mac}")
                
                # Provide troubleshooting tips
                print(f"\n{Colors.YELLOW}💡 Troubleshooting tips:{Colors.END}")
                if system == "Windows":
                    print(f"   • Try running as Administrator")
                    print(f"   • Check if interface supports MAC changes")
                    print(f"   • Restart the network adapter")
                else:
                    print(f"   • Try running with sudo")
                    print(f"   • Check if interface is managed by NetworkManager")
                    print(f"   • Ensure interface is not in use")
                
                sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Operation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()
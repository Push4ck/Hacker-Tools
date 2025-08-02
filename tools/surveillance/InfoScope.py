#!/usr/bin/env python3
"""
InfoScope - Professional Network Scanner
Cross-platform network discovery and device enumeration tool.
"""

import argparse
import platform
import subprocess
import socket
import threading
import ipaddress
import sys
import time
import json
import csv
from datetime import datetime
from typing import List, Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed


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
 ██╗███╗   ██╗███████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗
 ██║████╗  ██║██╔════╝██╔═══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║██╔██╗ ██║█████╗  ██║   ██║███████╗██║     ██║   ██║██████╔╝█████╗  
 ██║██║╚██╗██║██╔══╝  ██║   ██║╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝  
 ██║██║ ╚████║██║     ╚██████╔╝███████║╚██████╗╚██████╔╝██║     ███████╗
 ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝
{Colors.ENDC}
{Colors.BLUE}    Professional Network Discovery Tool v2.0{Colors.ENDC}
{Colors.CYAN}    Cross-Platform • Fast • Reliable{Colors.ENDC}
    {'─' * 60}
"""
    print(banner)


def check_network_connection(timeout: int = 3) -> bool:
    """
    Check if the system has an active network connection
    
    Args:
        timeout (int): Connection timeout in seconds
        
    Returns:
        bool: True if connected to network
    """
    test_hosts = [
        ("8.8.8.8", 53),      # Google DNS
        ("1.1.1.1", 53),      # Cloudflare DNS
        ("208.67.222.222", 53) # OpenDNS
    ]
    
    for host, port in test_hosts:
        try:
            socket.create_connection((host, port), timeout=timeout)
            return True
        except (socket.timeout, socket.error, OSError):
            continue
    
    return False


def ping_host(ip: str, timeout: int = 1) -> bool:
    """
    Ping a single host to check if it's alive
    
    Args:
        ip (str): IP address to ping
        timeout (int): Ping timeout in seconds
        
    Returns:
        bool: True if host responds to ping
    """
    try:
        system = platform.system().lower()
        
        if system == "windows":
            cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), str(ip)]
        else:  # Linux, macOS, etc.
            cmd = ["ping", "-c", "1", "-W", str(timeout), str(ip)]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        
        return result.returncode == 0
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        return False


def resolve_hostname(ip: str) -> str:
    """
    Resolve hostname for an IP address
    
    Args:
        ip (str): IP address to resolve
        
    Returns:
        str: Hostname or "Unknown" if resolution fails
    """
    try:
        hostname = socket.gethostbyaddr(str(ip))[0]
        return hostname
    except (socket.herror, socket.gaierror, socket.timeout):
        return "Unknown"


def get_device_info(ip: str) -> Dict[str, str]:
    """
    Get comprehensive information about a network device
    
    Args:
        ip (str): IP address of the device
        
    Returns:
        Dict[str, str]: Device information
    """
    hostname = resolve_hostname(ip)
    
    # Try to determine device type based on hostname or other characteristics
    device_type = "Unknown"
    if hostname != "Unknown":
        hostname_lower = hostname.lower()
        if any(x in hostname_lower for x in ['router', 'gateway', 'modem']):
            device_type = "Router/Gateway"
        elif any(x in hostname_lower for x in ['printer', 'print']):
            device_type = "Printer"
        elif any(x in hostname_lower for x in ['camera', 'cam', 'nvr']):
            device_type = "Camera/NVR"
        elif any(x in hostname_lower for x in ['phone', 'android', 'iphone']):
            device_type = "Mobile Device"
        elif any(x in hostname_lower for x in ['laptop', 'desktop', 'pc', 'workstation']):
            device_type = "Computer"
        else:
            device_type = "Network Device"
    
    return {
        'ip': str(ip),
        'hostname': hostname,
        'device_type': device_type,
        'status': 'Active'
    }


def scan_network_threaded(network: str, max_threads: int = 100, timeout: int = 1, verbose: bool = False) -> List[Dict[str, str]]:
    """
    Scan network using threading for improved performance
    
    Args:
        network (str): Network range in CIDR notation
        max_threads (int): Maximum number of concurrent threads
        timeout (int): Ping timeout in seconds
        verbose (bool): Enable verbose output
        
    Returns:
        List[Dict[str, str]]: List of active devices
    """
    try:
        network_obj = ipaddress.IPv4Network(network, strict=False)
        ip_list = list(network_obj.hosts()) if network_obj.num_addresses > 2 else [network_obj.network_address]
        
        if verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Scanning {len(ip_list)} IP addresses...")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Using {min(max_threads, len(ip_list))} concurrent threads")
        
        active_devices = []
        completed_scans = 0
        
        def scan_ip(ip):
            nonlocal completed_scans
            if ping_host(str(ip), timeout):
                device_info = get_device_info(str(ip))
                active_devices.append(device_info)
                if verbose:
                    print(f"{Colors.GREEN}[FOUND]{Colors.ENDC} {ip} - {device_info['hostname']}")
            
            completed_scans += 1
            if verbose and completed_scans % 50 == 0:
                progress = (completed_scans / len(ip_list)) * 100
                print(f"{Colors.CYAN}[PROGRESS]{Colors.ENDC} {completed_scans}/{len(ip_list)} ({progress:.1f}%)")
        
        # Use ThreadPoolExecutor for better thread management
        with ThreadPoolExecutor(max_workers=min(max_threads, len(ip_list))) as executor:
            futures = [executor.submit(scan_ip, ip) for ip in ip_list]
            
            # Wait for all threads to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    if verbose:
                        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Thread error: {str(e)}")
        
        return sorted(active_devices, key=lambda x: ipaddress.IPv4Address(x['ip']))
        
    except ValueError as e:
        raise ValueError(f"Invalid network format: {network}. Use CIDR notation (e.g., 192.168.1.0/24)")
    except Exception as e:
        raise Exception(f"Network scan failed: {str(e)}")


def display_results(devices: List[Dict[str, str]], show_stats: bool = True):
    """Display scan results in a formatted table"""
    if not devices:
        print(f"\n{Colors.YELLOW}[WARNING]{Colors.ENDC} No active devices found on the network.")
        return
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 NETWORK DISCOVERY RESULTS ({len(devices)} devices found){Colors.ENDC}")
    print("─" * 85)
    print(f"{Colors.BOLD}{'IP Address':<16} {'Hostname':<25} {'Device Type':<20} {'Status':<10}{Colors.ENDC}")
    print("─" * 85)
    
    # Group devices by type for better organization
    device_types = {}
    for device in devices:
        device_type = device['device_type']
        if device_type not in device_types:
            device_types[device_type] = []
        device_types[device_type].append(device)
    
    # Display devices grouped by type
    for device_type, type_devices in device_types.items():
        if len(device_types) > 1:
            print(f"\n{Colors.CYAN}[{device_type.upper()}]{Colors.ENDC}")
        
        for device in type_devices:
            ip_color = Colors.CYAN
            hostname_color = Colors.GREEN if device['hostname'] != "Unknown" else Colors.YELLOW
            type_color = Colors.BLUE
            status_color = Colors.GREEN
            
            print(f"{ip_color}{device['ip']:<16}{Colors.ENDC} "
                  f"{hostname_color}{device['hostname'][:24]:<25}{Colors.ENDC} "
                  f"{type_color}{device['device_type']:<20}{Colors.ENDC} "
                  f"{status_color}{device['status']:<10}{Colors.ENDC}")
    
    print("─" * 85)
    
    if show_stats:
        # Display statistics
        total_devices = len(devices)
        known_hostnames = sum(1 for d in devices if d['hostname'] != "Unknown")
        
        print(f"\n{Colors.BLUE}[STATISTICS]{Colors.ENDC}")
        print(f"  • Total active devices: {Colors.GREEN}{total_devices}{Colors.ENDC}")
        print(f"  • Resolved hostnames: {Colors.GREEN}{known_hostnames}{Colors.ENDC} ({(known_hostnames/total_devices)*100:.1f}%)")
        print(f"  • Device types identified: {Colors.GREEN}{len(device_types)}{Colors.ENDC}")


def save_results(file_path: str, devices: List[Dict[str, str]], network: str, scan_time: float):
    """Save results to file based on extension"""
    if not devices:
        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} No data to save.")
        return
    
    try:
        file_format = file_path.split('.')[-1].lower()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if file_format == 'json':
            _save_to_json(file_path, devices, network, timestamp, scan_time)
        elif file_format == 'csv':
            _save_to_csv(file_path, devices)
        elif file_format == 'txt':
            _save_to_txt(file_path, devices, network, timestamp, scan_time)
        elif file_format == 'html':
            _save_to_html(file_path, devices, network, timestamp, scan_time)
        else:
            raise ValueError(f"Unsupported format: {file_format}")
        
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Results saved to: {file_path}")
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to save file: {str(e)}")


def _save_to_json(file_path: str, devices: List[Dict[str, str]], network: str, timestamp: str, scan_time: float):
    """Save data to JSON file"""
    output = {
        "scan_info": {
            "timestamp": timestamp,
            "network": network,
            "scan_duration": f"{scan_time:.2f} seconds",
            "total_devices": len(devices)
        },
        "devices": devices
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def _save_to_csv(file_path: str, devices: List[Dict[str, str]]):
    """Save data to CSV file"""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['ip', 'hostname', 'device_type', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(devices)


def _save_to_txt(file_path: str, devices: List[Dict[str, str]], network: str, timestamp: str, scan_time: float):
    """Save data to text file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"InfoScope Network Scan Results\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(f"Scan Date: {timestamp}\n")
        f.write(f"Network: {network}\n")
        f.write(f"Scan Duration: {scan_time:.2f} seconds\n")
        f.write(f"Devices Found: {len(devices)}\n\n")
        f.write(f"{'IP Address':<16} {'Hostname':<25} {'Device Type':<20} {'Status'}\n")
        f.write(f"{'-' * 75}\n")
        
        for device in devices:
            f.write(f"{device['ip']:<16} {device['hostname']:<25} {device['device_type']:<20} {device['status']}\n")


def _save_to_html(file_path: str, devices: List[Dict[str, str]], network: str, timestamp: str, scan_time: float):
    """Save data to HTML file"""
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InfoScope Network Scan Results</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .info {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: #3498db; color: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 InfoScope Network Scan Results</h1>
        
        <div class="info">
            <strong>Scan Information:</strong><br>
            <strong>Date:</strong> {timestamp}<br>
            <strong>Network:</strong> {network}<br>
            <strong>Duration:</strong> {scan_time:.2f} seconds<br>
            <strong>Devices Found:</strong> {len(devices)}
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <h3>{len(devices)}</h3>
                <p>Active Devices</p>
            </div>
            <div class="stat-box">
                <h3>{sum(1 for d in devices if d['hostname'] != 'Unknown')}</h3>
                <p>Resolved Hostnames</p>
            </div>
            <div class="stat-box">
                <h3>{len(set(d['device_type'] for d in devices))}</h3>
                <p>Device Types</p>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>IP Address</th>
                    <th>Hostname</th>
                    <th>Device Type</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>"""
    
    for device in devices:
        html_template += f"""
                <tr>
                    <td>{device['ip']}</td>
                    <td>{device['hostname']}</td>
                    <td>{device['device_type']}</td>
                    <td>{device['status']}</td>
                </tr>"""
    
    html_template += """
            </tbody>
        </table>
    </div>
</body>
</html>"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)


def get_local_network():
    """Attempt to determine the local network range"""
    try:
        # Get the default route
        if platform.system().lower() == "windows":
            result = subprocess.run(['route', 'print', '0.0.0.0'], 
                                   capture_output=True, text=True)
        else:
            result = subprocess.run(['ip', 'route'], 
                                   capture_output=True, text=True)
        
        # This is a simplified approach - in practice, you'd parse the routing table
        # For now, return common network ranges
        return "192.168.1.0/24"
        
    except:
        return "192.168.1.0/24"


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='InfoScope',
        description='Professional cross-platform network discovery tool',
        epilog='''
Examples:
  %(prog)s                                          # Scan default network (192.168.1.0/24)
  %(prog)s -n 192.168.0.0/24                       # Scan specific network
  %(prog)s -n 10.0.0.0/24 --verbose                # Verbose scanning
  %(prog)s -n 192.168.1.0/24 -o results.json       # Save to JSON
  %(prog)s -n 192.168.1.0/24 -o report.html -v     # HTML report with verbose
  %(prog)s -n 192.168.1.1-50                       # Scan IP range
  %(prog)s --threads 200 --timeout 2               # High-speed scan

Supported output formats: json, csv, txt, html
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-n', '--network',
        metavar='RANGE',
        default='192.168.1.0/24',
        help='Network range to scan in CIDR notation (default: 192.168.1.0/24)'
    )
    
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='Save results to file (format: json, csv, txt, html)'
    )
    
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=100,
        metavar='N',
        help='Maximum number of concurrent threads (default: 100)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=1,
        metavar='SEC',
        help='Ping timeout in seconds (default: 1)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output with progress information'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Suppress banner display'
    )
    
    parser.add_argument(
        '--no-stats',
        action='store_true',
        help='Suppress statistics display'
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
    
    # Check network connectivity
    if args.verbose:
        print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Checking network connectivity...")
    
    if not check_network_connection():
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} No network connection detected. Please check your network settings.")
        sys.exit(1)
    
    if args.verbose:
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Network connection confirmed")
    
    # Validate thread count
    if args.threads < 1 or args.threads > 1000:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Thread count must be between 1 and 1000")
        sys.exit(1)
    
    # Validate timeout
    if args.timeout < 1 or args.timeout > 10:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Timeout must be between 1 and 10 seconds")
        sys.exit(1)
    
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Starting network scan: {args.network}")
    
    start_time = time.time()
    
    try:
        # Perform network scan
        devices = scan_network_threaded(
            args.network, 
            max_threads=args.threads,
            timeout=args.timeout,
            verbose=args.verbose
        )
        
        scan_time = time.time() - start_time
        
        # Display results
        display_results(devices, show_stats=not args.no_stats)
        
        if args.verbose or not devices:
            print(f"\n{Colors.CYAN}[INFO]{Colors.ENDC} Scan completed in {scan_time:.2f} seconds")
        
        # Save results if output file specified
        if args.output:
            save_results(args.output, devices, args.network, scan_time)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.ENDC} Scan interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.ENDC} {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
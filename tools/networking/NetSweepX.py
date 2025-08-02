#!/usr/bin/env python3
"""
NetSweepX - Professional Network Scanner
A fast and reliable tool for network discovery and device enumeration.
"""

import scapy.all as scapy
import argparse
import socket
import json
import csv
import sys
import os
import subprocess
import re
import ipaddress
from datetime import datetime
from typing import List, Dict, Any


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Display the application banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ███╗   ██╗███████╗████████╗███████╗██╗    ██╗███████╗███████╗██████╗ ██╗  ██╗
 ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗╚██╗██╔╝
 ██╔██╗ ██║█████╗     ██║   ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝ ╚███╔╝ 
 ██║╚██╗██║██╔══╝     ██║   ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝  ██╔██╗ 
 ██║ ╚████║███████╗   ██║   ███████║╚███╔███╔╝███████╗███████╗██║     ██╔╝ ██╗
 ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BLUE}    Professional Network Discovery Tool v2.0{Colors.ENDC}
{Colors.CYAN}    Fast • Reliable • Cross-Platform{Colors.ENDC}
    {'─' * 63}
"""
    print(banner)


def scan_network(target_ip: str, verbose: bool = False) -> List[Dict[str, str]]:
    """
    Scan the network for active devices using ARP requests
    
    Args:
        target_ip (str): IP address or CIDR range to scan
        verbose (bool): Enable verbose output
        
    Returns:
        List[Dict[str, str]]: List of discovered devices
        
    Raises:
        Exception: If scanning fails
    """
    try:
        if verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Scanning network: {target_ip}")
            
        devices = []
        
        # Try layer 2 ARP scanning first
        try:
            # Create ARP request
            arp_request = scapy.ARP(pdst=target_ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            
            # Send packet and capture responses
            answered_list = scapy.srp(
                arp_request/broadcast, 
                timeout=2, 
                verbose=False,
                retry=1
            )[0]

            for sent, received in answered_list:
                try:
                    # Attempt to resolve hostname
                    hostname = socket.gethostbyaddr(received.psrc)[0]
                except (socket.herror, socket.gaierror, socket.timeout):
                    hostname = "Unknown"
                    
                device = {
                    "ip": received.psrc,
                    "mac": received.hwsrc,
                    "hostname": hostname
                }
                devices.append(device)
                
        except Exception as layer2_error:
            # Fallback to layer 3 scanning (ping sweep + ARP table)
            if verbose:
                print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} Layer 2 scanning failed, using layer 3 fallback")
            
            devices = _layer3_scan(target_ip, verbose)
            
        return devices
        
    except PermissionError:
        raise Exception("Permission denied. Please run as administrator/root for network scanning.")
    except Exception as e:
        raise Exception(f"Network scan failed: {str(e)}")


def _layer3_scan(target_ip: str, verbose: bool = False) -> List[Dict[str, str]]:
    """
    Fallback layer 3 scanning using ICMP ping and ARP table lookup
    """
    import ipaddress
    import subprocess
    import re
    
    devices = []
    
    try:
        # Parse the target IP range
        if '/' in target_ip:
            network = ipaddress.IPv4Network(target_ip, strict=False)
            ip_list = list(network.hosts())
        elif '-' in target_ip:
            # Handle range like 192.168.1.1-50
            base_ip, end_range = target_ip.split('-')
            base_parts = base_ip.split('.')
            start_ip = int(base_parts[3])
            end_ip = int(end_range)
            ip_list = []
            for i in range(start_ip, end_ip + 1):
                ip_list.append(ipaddress.IPv4Address(f"{'.'.join(base_parts[:3])}.{i}"))
        else:
            # Single IP
            ip_list = [ipaddress.IPv4Address(target_ip)]
        
        if verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Scanning {len(ip_list)} IP addresses...")
        
        # Ping sweep to populate ARP table
        active_ips = []
        for ip in ip_list:
            try:
                # Use ping to check if host is alive
                if os.name == 'nt':  # Windows
                    result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], 
                                          capture_output=True, text=True, timeout=2)
                else:  # Linux/Mac
                    result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                          capture_output=True, text=True, timeout=2)
                
                if result.returncode == 0:
                    active_ips.append(str(ip))
                    
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                continue
        
        if verbose:
            print(f"{Colors.GREEN}[INFO]{Colors.ENDC} Found {len(active_ips)} active IPs, retrieving MAC addresses...")
        
        # Get ARP table to find MAC addresses
        arp_table = _get_arp_table()
        
        for ip in active_ips:
            try:
                # Get hostname
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except (socket.herror, socket.gaierror, socket.timeout):
                    hostname = "Unknown"
                
                # Get MAC from ARP table
                mac = arp_table.get(ip, "Unknown")
                
                device = {
                    "ip": ip,
                    "mac": mac,
                    "hostname": hostname
                }
                devices.append(device)
                
            except Exception:
                continue
                
    except Exception as e:
        if verbose:
            print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} Layer 3 scan error: {str(e)}")
    
    return devices


def _get_arp_table() -> Dict[str, str]:
    """
    Get the system ARP table to find MAC addresses
    """
    arp_table = {}
    
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                # Parse Windows ARP table format
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9-]{17})', line)
                if match:
                    ip, mac = match.groups()
                    arp_table[ip] = mac.replace('-', ':').lower()
        else:  # Linux/Mac
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                # Parse Unix ARP table format
                match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\) at ([a-fA-F0-9:]{17})', line)
                if match:
                    ip, mac = match.groups()
                    arp_table[ip] = mac.lower()
                    
    except Exception:
        pass
    
    return arp_table


def display_results(devices: List[Dict[str, str]], verbose: bool = False):
    """Display scan results in a formatted table"""
    if not devices:
        print(f"\n{Colors.WARNING}[WARNING]{Colors.ENDC} No devices found on the network.")
        return
        
    print(f"\n{Colors.GREEN}{Colors.BOLD}📡 DISCOVERED DEVICES ({len(devices)} found){Colors.ENDC}")
    print("─" * 80)
    print(f"{Colors.BOLD}{'IP Address':<16} {'MAC Address':<18} {'Hostname':<25}{Colors.ENDC}")
    print("─" * 80)
    
    for device in devices:
        ip_color = Colors.CYAN if device['ip'] else Colors.WARNING
        mac_color = Colors.BLUE if device['mac'] else Colors.WARNING  
        hostname_color = Colors.GREEN if device['hostname'] != "Unknown" else Colors.WARNING
        
        print(f"{ip_color}{device['ip']:<16}{Colors.ENDC} "
              f"{mac_color}{device['mac']:<18}{Colors.ENDC} "
              f"{hostname_color}{device['hostname']:<25}{Colors.ENDC}")
    
    print("─" * 80)


def save_results(file_path: str, data: List[Dict[str, str]], verbose: bool = False):
    """Save results to file based on extension"""
    if not data:
        print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} No data to save.")
        return
        
    try:
        file_format = file_path.split('.')[-1].lower()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if file_format == 'txt':
            _save_to_txt(file_path, data, timestamp)
        elif file_format == 'json':
            _save_to_json(file_path, data, timestamp)
        elif file_format == 'csv':
            _save_to_csv(file_path, data)
        elif file_format == 'html':
            _save_to_html(file_path, data, timestamp)
        elif file_format in ['xml', 'pcap']:
            _save_to_pcap(file_path, data)
        else:
            raise ValueError(f"Unsupported format: {file_format}")
            
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Results saved to: {file_path}")
        
    except FileExistsError:
        print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} File already exists: {file_path}")
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} Failed to save file: {str(e)}")


def _save_to_txt(file_path: str, data: List[Dict[str, str]], timestamp: str):
    """Save data to text file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"NetSweepX Results - {timestamp}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"{'IP Address':<16} {'MAC Address':<18} {'Hostname'}\n")
        f.write("-" * 50 + "\n")
        
        for device in data:
            f.write(f"{device['ip']:<16} {device['mac']:<18} {device['hostname']}\n")


def _save_to_json(file_path: str, data: List[Dict[str, str]], timestamp: str):
    """Save data to JSON file"""
    output = {
        "scan_timestamp": timestamp,
        "total_devices": len(data),
        "devices": data
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def _save_to_csv(file_path: str, data: List[Dict[str, str]]):
    """Save data to CSV file"""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['ip', 'mac', 'hostname'])
        writer.writeheader()
        writer.writerows(data)


def _save_to_html(file_path: str, data: List[Dict[str, str]], timestamp: str):
    """Save data to HTML file"""
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetSweepX Results</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .timestamp {{ color: #7f8c8d; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 NetSweepX Results</h1>
        <p class="timestamp">Scan performed: {timestamp}</p>
        <p><strong>Total devices found:</strong> {len(data)}</p>
        
        <table>
            <thead>
                <tr>
                    <th>IP Address</th>
                    <th>MAC Address</th>
                    <th>Hostname</th>
                </tr>
            </thead>
            <tbody>"""
    
    for device in data:
        html_template += f"""
                <tr>
                    <td>{device['ip']}</td>
                    <td>{device['mac']}</td>
                    <td>{device['hostname']}</td>
                </tr>"""
    
    html_template += """
            </tbody>
        </table>
    </div>
</body>
</html>"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)


def _save_to_pcap(file_path: str, data: List[Dict[str, str]]):
    """Save data to PCAP file"""
    packets = []
    for device in data:
        packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(
            psrc=device['ip'], 
            hwsrc=device['mac']
        )
        packets.append(packet)
    
    scapy.wrpcap(file_path, packets)


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='NetSweepX',
        description='Professional network scanner for device discovery',
        epilog='''
Examples:
  %(prog)s -t 192.168.1.0/24                    # Scan entire subnet
  %(prog)s -t 192.168.1.1                       # Scan single IP
  %(prog)s -t 192.168.1.1-50                    # Scan IP range
  %(prog)s -t 192.168.1.0/24 -o results.json    # Save to JSON
  %(prog)s -t 192.168.1.0/24 -v                 # Verbose output
  %(prog)s -t 192.168.1.0/24 -o report.html -v  # HTML report with verbose

Supported output formats: txt, json, csv, html, pcap
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-t', '--target',
        dest='target',
        required=True,
        metavar='TARGET',
        help='IP address, CIDR range, or IP range to scan (e.g., 192.168.1.0/24)'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output',
        metavar='FILE',
        help='Save results to file (format determined by extension: .txt, .json, .csv, .html, .pcap)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output with timing information'
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


def validate_target(target: str) -> bool:
    """Basic validation for target IP/range format"""
    try:
        # Basic validation - scapy will handle the detailed parsing
        if '/' in target or '-' in target or target.count('.') == 3:
            return True
        return False
    except:
        return False


def main():
    """Main application entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Display banner unless suppressed
    if not args.no_banner:
        print_banner()
    
    # Validate target
    if not validate_target(args.target):
        print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} Invalid target format: {args.target}")
        print("Use formats like: 192.168.1.0/24, 192.168.1.1, or 192.168.1.1-50")
        sys.exit(1)
    
    # Check for root/admin privileges
    if os.name != 'nt' and os.geteuid() != 0:
        print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} Running without root privileges may limit functionality.")
    
    start_time = datetime.now()
    
    try:
        if args.verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Starting network scan...")
            
        # Perform scan
        devices = scan_network(args.target, args.verbose)
        
        # Calculate scan time
        end_time = datetime.now()
        scan_duration = (end_time - start_time).total_seconds()
        
        # Display results
        display_results(devices, args.verbose)
        
        if args.verbose:
            print(f"\n{Colors.GREEN}[INFO]{Colors.ENDC} Scan completed in {scan_duration:.2f} seconds")
        
        # Save results if output file specified
        if args.output:
            save_results(args.output, devices, args.verbose)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[INTERRUPTED]{Colors.ENDC} Scan interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}[ERROR]{Colors.ENDC} {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
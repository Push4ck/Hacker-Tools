#!/usr/bin/env python3
"""
Gatekeeper - Professional Network Security Testing Suite
Advanced network connectivity analysis and penetration testing tools
"""

import socket
import argparse
import sys
import threading
import time
import platform
import ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional, Dict

# Constants
__version__ = "4.0.0"
__author__ = "Gatekeeper Security Team"

class Style:
    """Professional styling system for security tools"""
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Security symbols
    SHIELD = '🛡️'
    TARGET = '🎯'
    SCAN = '🔍'
    NETWORK = '🌐'
    LOCK = '🔒'
    UNLOCK = '🔓'
    WARNING = '⚠️'
    SUCCESS = '✅'
    FAILED = '❌'
    HAMMER = '🔨'
    
    @classmethod
    def init_colors(cls):
        """Initialize cross-platform color support"""
        if platform.system() == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                for attr in dir(cls):
                    if not attr.startswith('_') and attr.isupper() and len(getattr(cls, attr)) > 1:
                        setattr(cls, attr, '')

# Initialize styling
Style.init_colors()

def print_header():
    """Display professional security tool header"""
    width = 80
    header = f"""
{Style.CYAN}{Style.BOLD}{'=' * width}
{'Gatekeeper'.center(width)}
{'Professional Network Security Testing Suite'.center(width)}
{Style.RESET}{Style.CYAN}{'=' * width}{Style.RESET}

{Style.WHITE}{Style.BOLD}Version:{Style.RESET} {Style.CYAN}{__version__}{Style.RESET}  {Style.GRAY}|{Style.RESET}  {Style.WHITE}{Style.BOLD}Platform:{Style.RESET} {Style.CYAN}{platform.system()}{Style.RESET}  {Style.GRAY}|{Style.RESET}  {Style.WHITE}{Style.BOLD}Purpose:{Style.RESET} {Style.GREEN}Penetration Testing{Style.RESET}

{Style.YELLOW}{Style.ITALIC}"Advanced network reconnaissance and security assessment tools"{Style.RESET}
"""
    print(header)

def print_success(message: str, symbol: str = Style.SUCCESS):
    """Print success message with styling"""
    print(f"{Style.GREEN}{Style.BOLD}[SUCCESS]{Style.RESET} {symbol} {message}")

def print_error(message: str, symbol: str = Style.FAILED):
    """Print error message with styling"""
    print(f"{Style.RED}{Style.BOLD}[ERROR]{Style.RESET} {symbol} {message}")

def print_info(message: str, symbol: str = "ℹ️"):
    """Print info message with styling"""
    print(f"{Style.BLUE}{Style.BOLD}[INFO]{Style.RESET} {symbol} {message}")

def print_warning(message: str, symbol: str = Style.WARNING):
    """Print warning message with styling"""
    print(f"{Style.YELLOW}{Style.BOLD}[WARNING]{Style.RESET} {symbol} {message}")

def print_scan_result(host: str, port: int, status: str, service: str = ""):
    """Print formatted scan result"""
    status_color = Style.GREEN if status == "OPEN" else Style.RED
    status_symbol = Style.UNLOCK if status == "OPEN" else Style.LOCK
    
    service_info = f" ({service})" if service else ""
    print(f"  {status_color}{status_symbol} {host}:{port}{Style.RESET} - {status_color}{Style.BOLD}{status}{Style.RESET}{service_info}")

def print_separator(char: str = "─", length: int = 60):
    """Print visual separator"""
    print(f"{Style.GRAY}{char * length}{Style.RESET}")

def animate_scan(message: str, duration: float = 1.0):
    """Animate scanning operations"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    
    while time.time() < end_time:
        print(f"\r{Style.CYAN}{frames[i % len(frames)]}{Style.RESET} {message}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    
    print(f"\r{Style.GREEN}✓{Style.RESET} {message}")

class NetworkScanner:
    """Professional network scanning and analysis toolkit"""
    
    def __init__(self):
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            1723: "PPTP", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Proxy"
        }
    
    def check_single_port(self, host: str, port: int, timeout: float = 2.0) -> Tuple[bool, str]:
        """
        Check if a single port is open on a target host
        
        Args:
            host: Target IP address or hostname
            port: Port number to check
            timeout: Connection timeout in seconds
            
        Returns:
            Tuple of (is_open, service_name)
        """
        try:
            with socket.create_connection((host, port), timeout=timeout):
                service = self.common_ports.get(port, "Unknown")
                return True, service
        except (socket.timeout, socket.error, ConnectionRefusedError):
            return False, ""
    
    def scan_port_range(self, host: str, start_port: int, end_port: int, 
                       timeout: float = 1.0, max_threads: int = 50) -> Dict[int, Tuple[bool, str]]:
        """
        Scan a range of ports on a target host
        
        Args:
            host: Target IP address or hostname
            start_port: Starting port number
            end_port: Ending port number
            timeout: Connection timeout per port
            max_threads: Maximum concurrent threads
            
        Returns:
            Dictionary mapping port numbers to (is_open, service) tuples
        """
        results = {}
        
        def scan_port(port):
            is_open, service = self.check_single_port(host, port, timeout)
            return port, is_open, service
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(scan_port, port) for port in range(start_port, end_port + 1)]
            
            for future in as_completed(futures):
                port, is_open, service = future.result()
                results[port] = (is_open, service)
        
        return results
    
    def scan_common_ports(self, host: str, timeout: float = 1.0) -> Dict[int, Tuple[bool, str]]:
        """Scan commonly used ports"""
        return {port: self.check_single_port(host, port, timeout) 
                for port in self.common_ports.keys()}
    
    def banner_grab(self, host: str, port: int, timeout: float = 3.0) -> Optional[str]:
        """
        Attempt to grab service banner from an open port
        
        Args:
            host: Target IP address or hostname  
            port: Port number to connect to
            timeout: Connection timeout
            
        Returns:
            Service banner string or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Try to receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
            
        except Exception:
            return None
    
    def validate_target(self, target: str) -> bool:
        """Validate if target is a valid IP address or hostname"""
        try:
            # Try as IP address first
            ipaddress.ip_address(target)
            return True
        except ValueError:
            # Try as hostname
            try:
                socket.gethostbyname(target)
                return True
            except socket.gaierror:
                return False

def display_scan_summary(results: Dict[int, Tuple[bool, str]], host: str):
    """Display comprehensive scan results summary"""
    open_ports = {port: (status, service) for port, (status, service) in results.items() if status}
    closed_ports = len([port for port, (status, _) in results.items() if not status])
    
    print_separator("═")
    print(f"{Style.WHITE}{Style.BOLD}📊 SCAN RESULTS SUMMARY{Style.RESET}")
    print_separator("═")
    
    summary_data = [
        ("Target Host", f"{Style.BOLD}{host}{Style.RESET}"),
        ("Total Ports Scanned", f"{Style.BOLD}{len(results):,}{Style.RESET}"),
        ("Open Ports", f"{Style.GREEN}{Style.BOLD}{len(open_ports)}{Style.RESET}"),
        ("Closed Ports", f"{Style.RED}{Style.BOLD}{closed_ports}{Style.RESET}"),
        ("Scan Timestamp", f"{Style.BOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET}")
    ]
    
    for label, value in summary_data:
        print(f"  {Style.CYAN}{Style.BOLD}{label:.<20}{Style.RESET} {value}")
    
    if open_ports:
        print_separator()
        print(f"{Style.GREEN}{Style.BOLD}🔓 OPEN PORTS DETECTED:{Style.RESET}")
        print_separator()
        
        for port, (_, service) in sorted(open_ports.items()):
            print_scan_result(host, port, "OPEN", service)
    
    print_separator("═")

def perform_single_port_check(host: str, port: int, timeout: float, banner_grab: bool = False):
    """Perform detailed single port analysis"""
    print_header()
    
    scanner = NetworkScanner()
    
    # Validate target
    if not scanner.validate_target(host):
        print_error(f"Invalid target: {host}")
        print_info("Please provide a valid IP address or hostname")
        return False
    
    print(f"{Style.WHITE}{Style.BOLD}🎯 TARGET ANALYSIS{Style.RESET}")
    print_separator()
    print(f"  {Style.CYAN}{Style.BOLD}Target Host....{Style.RESET} {host}")
    print(f"  {Style.CYAN}{Style.BOLD}Target Port....{Style.RESET} {port}")
    print(f"  {Style.CYAN}{Style.BOLD}Timeout........{Style.RESET} {timeout}s")
    print_separator()
    
    # Perform scan
    animate_scan(f"Scanning {host}:{port}")
    
    is_open, service = scanner.check_single_port(host, port, timeout)
    
    print()
    if is_open:
        print_success(f"Port {port} is OPEN on {host}")
        if service != "Unknown":
            print_info(f"Detected service: {service}")
        
        # Banner grabbing
        if banner_grab:
            animate_scan("Attempting banner grab", 1.5)
            banner = scanner.banner_grab(host, port)
            if banner:
                print_info(f"Service banner: {Style.BOLD}{banner[:100]}{Style.RESET}")
            else:
                print_warning("No banner received")
    else:
        print_error(f"Port {port} is CLOSED or filtered on {host}")
    
    return is_open

def perform_port_scan(host: str, start_port: int, end_port: int, timeout: float, threads: int):
    """Perform comprehensive port range scanning"""
    print_header()
    
    scanner = NetworkScanner()
    
    # Validate target
    if not scanner.validate_target(host):
        print_error(f"Invalid target: {host}")
        return False
    
    port_count = end_port - start_port + 1
    
    print(f"{Style.WHITE}{Style.BOLD}🔍 PORT SCAN CONFIGURATION{Style.RESET}")
    print_separator()
    print(f"  {Style.CYAN}{Style.BOLD}Target Host....{Style.RESET} {host}")
    print(f"  {Style.CYAN}{Style.BOLD}Port Range.....{Style.RESET} {start_port}-{end_port}")
    print(f"  {Style.CYAN}{Style.BOLD}Total Ports....{Style.RESET} {port_count:,}")
    print(f"  {Style.CYAN}{Style.BOLD}Timeout........{Style.RESET} {timeout}s")
    print(f"  {Style.CYAN}{Style.BOLD}Threads........{Style.RESET} {threads}")
    print_separator()
    
    # Perform scan
    print(f"\n{Style.YELLOW}{Style.BOLD}🚀 INITIATING PORT SCAN{Style.RESET}")
    start_time = time.time()
    
    results = scanner.scan_port_range(host, start_port, end_port, timeout, threads)
    
    scan_duration = time.time() - start_time
    
    print(f"\n{Style.GREEN}{Style.BOLD}✓ Scan completed in {scan_duration:.2f} seconds{Style.RESET}")
    
    # Display results
    display_scan_summary(results, host)
    
    return True

def perform_common_ports_scan(host: str, timeout: float):
    """Scan commonly used ports"""
    print_header()
    
    scanner = NetworkScanner()
    
    if not scanner.validate_target(host):
        print_error(f"Invalid target: {host}")
        return False
    
    print(f"{Style.WHITE}{Style.BOLD}🔍 COMMON PORTS SCAN{Style.RESET}")
    print_separator()
    print(f"  {Style.CYAN}{Style.BOLD}Target Host....{Style.RESET} {host}")
    print(f"  {Style.CYAN}{Style.BOLD}Port Count.....{Style.RESET} {len(scanner.common_ports)} common ports")
    print(f"  {Style.CYAN}{Style.BOLD}Timeout........{Style.RESET} {timeout}s")
    print_separator()
    
    print(f"\n{Style.YELLOW}{Style.BOLD}🚀 SCANNING COMMON PORTS{Style.RESET}")
    start_time = time.time()
    
    results = scanner.scan_common_ports(host, timeout)
    
    scan_duration = time.time() - start_time
    print(f"\n{Style.GREEN}{Style.BOLD}✓ Scan completed in {scan_duration:.2f} seconds{Style.RESET}")
    
    display_scan_summary(results, host)
    
    return True

def create_argument_parser():
    """Create comprehensive argument parser for security testing"""
    
    description = f"""
{Style.BOLD}Gatekeeper v{__version__}{Style.RESET} - Professional Network Security Testing Suite

A comprehensive penetration testing toolkit for network reconnaissance, port scanning,
and service enumeration. Designed for ethical hackers, penetration testers, and 
cybersecurity professionals working on authorized systems.

{Style.BOLD}Perfect for:{Style.RESET}
  • TryHackMe challenges and CTF competitions
  • Penetration testing engagements  
  • Network security assessments
  • Educational cybersecurity training
"""
    
    epilog = f"""
{Style.BOLD}Usage Examples:{Style.RESET}
  gatekeeper -H 10.10.10.100 -p 22                    # Check single port
  gatekeeper -H target.thm -r 1-1000                  # Scan port range
  gatekeeper -H 192.168.1.1 --common                  # Scan common ports
  gatekeeper -H example.com -p 80 --banner            # Banner grabbing
  gatekeeper -H 10.0.0.1 -r 80-443 -t 0.5 --threads 100  # Fast scan

{Style.BOLD}Scan Types:{Style.RESET}
  Single Port    : Detailed analysis of specific port
  Range Scan     : Comprehensive scanning of port ranges
  Common Ports   : Quick scan of frequently used ports
  Banner Grab    : Service fingerprinting and enumeration

{Style.BOLD}Security Notice:{Style.RESET}
  This tool is for authorized testing only. Always ensure you have explicit
  permission before scanning any systems. Unauthorized scanning may be illegal.

{Style.CYAN}Happy hacking! 🛡️{Style.RESET}
"""
    
    parser = argparse.ArgumentParser(
        prog='gatekeeper',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Target specification
    target_group = parser.add_argument_group(f'{Style.BOLD}Target Specification{Style.RESET}')
    target_group.add_argument('-H', '--host', required=True, metavar='HOST',
                             help='Target IP address or hostname')
    
    # Scan type selection (mutually exclusive)
    scan_group = parser.add_argument_group(f'{Style.BOLD}Scan Configuration{Style.RESET}')
    scan_type = scan_group.add_mutually_exclusive_group(required=True)
    scan_type.add_argument('-p', '--port', type=int, metavar='PORT',
                          help='Single port to check')
    scan_type.add_argument('-r', '--range', metavar='START-END',
                          help='Port range to scan (e.g., 1-1000)')
    scan_type.add_argument('--common', action='store_true',
                          help='Scan common ports only')
    
    # Scan parameters
    params_group = parser.add_argument_group(f'{Style.BOLD}Scan Parameters{Style.RESET}')
    params_group.add_argument('-t', '--timeout', type=float, default=2.0, metavar='SEC',
                             help='Connection timeout in seconds (default: 2.0)')
    params_group.add_argument('--threads', type=int, default=50, metavar='N',
                             help='Number of concurrent threads (default: 50)')
    params_group.add_argument('--banner', action='store_true',
                             help='Attempt banner grabbing on open ports')
    
    # Utility options
    utils_group = parser.add_argument_group(f'{Style.BOLD}Utility Options{Style.RESET}')
    utils_group.add_argument('--no-header', action='store_true',
                            help='Skip application header')
    utils_group.add_argument('--version', action='version',
                            version=f'Gatekeeper {__version__}')
    
    return parser

def main():
    """Main application entry point for security testing"""
    parser = create_argument_parser()
    
    # Handle no arguments
    if len(sys.argv) == 1:
        print_header()
        print(f"{Style.YELLOW}{Style.BOLD}Welcome to Gatekeeper Security Suite!{Style.RESET}")
        print(f"{Style.GRAY}Use --help for detailed usage information{Style.RESET}\n")
        parser.print_help()
        sys.exit(0)
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)
    
    # Validate thread count
    if args.threads < 1 or args.threads > 200:
        print_error("Thread count must be between 1 and 200")
        sys.exit(1)
    
    # Validate timeout
    if args.timeout <= 0 or args.timeout > 30:
        print_error("Timeout must be between 0.1 and 30 seconds")
        sys.exit(1)
    
    success = False
    
    try:
        # Execute appropriate scan type
        if args.port:
            # Single port check
            success = perform_single_port_check(args.host, args.port, args.timeout, args.banner)
            
        elif args.range:
            # Port range scan
            try:
                start_port, end_port = map(int, args.range.split('-'))
                if start_port < 1 or end_port > 65535 or start_port > end_port:
                    raise ValueError("Invalid port range")
                success = perform_port_scan(args.host, start_port, end_port, args.timeout, args.threads)
            except ValueError:
                print_error("Invalid port range format. Use: START-END (e.g., 1-1000)")
                sys.exit(1)
                
        elif args.common:
            # Common ports scan
            success = perform_common_ports_scan(args.host, args.timeout)
        
        # Display completion message
        if success:
            print(f"\n{Style.GREEN}{Style.BOLD}🎯 Reconnaissance mission completed successfully!{Style.RESET}")
            sys.exit(0)
        else:
            print(f"\n{Style.RED}{Style.BOLD}💥 Operation failed. Check target accessibility.{Style.RESET}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Style.YELLOW}{Style.BOLD}🛑 Scan interrupted by user{Style.RESET}")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
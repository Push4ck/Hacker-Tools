#!/usr/bin/env python3
"""
PenTest Request Tool - Educational Security Testing
A controlled HTTP testing tool for authorized penetration testing and CTF challenges.
"""

import argparse
import requests
import logging
import time
import sys
import os
import urllib.parse
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor, as_completed
import json


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
    """Display the application banner with ethical use notice"""
    Colors.disable_on_windows()
    
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                    PenTest Request Tool v1.0                ║
║              Educational Security Testing Framework          ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.YELLOW}⚖️  AUTHORIZED TESTING ONLY: This tool is designed for:
   • TryHackMe and CTF challenges
   • Authorized penetration testing
   • Your own lab environments
   • Educational security research{Colors.END}

{Colors.RED}🚫 DO NOT use against systems you don't own or have explicit permission to test!{Colors.END}

{Colors.BLUE}🎯 Multi-proxy HTTP request testing with rate limiting
📊 Response analysis and vulnerability detection patterns
🔧 Customizable headers, payloads, and request patterns{Colors.END}
"""
    print(banner)


def setup_logging(log_level, log_file=None):
    """Configure logging with appropriate level and output"""
    log_format = f'{Colors.CYAN}%(asctime)s{Colors.END} - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            *([logging.FileHandler(log_file)] if log_file else [])
        ]
    )
    
    return logging.getLogger(__name__)


def validate_target_url(url):
    """Validate and sanitize target URL"""
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        
        # Check for common lab/CTF domains
        allowed_patterns = [
            'tryhackme.com',
            '10.10.10.',  # HTB
            '10.10.11.',  # HTB
            'localhost',
            '127.0.0.1',
            '192.168.',   # Local network
            '.local',     # Local domains
            'ctf.',       # CTF domains
            'lab.',       # Lab domains
        ]
        
        is_lab_domain = any(pattern in url.lower() for pattern in allowed_patterns)
        
        if not is_lab_domain:
            print(f"{Colors.YELLOW}⚠️  Warning: Target doesn't appear to be a lab environment.{Colors.END}")
            print(f"{Colors.YELLOW}   Ensure you have permission to test: {url}{Colors.END}")
            
            response = input(f"{Colors.CYAN}Continue? (yes/no): {Colors.END}").lower()
            if response not in ['yes', 'y']:
                print(f"{Colors.RED}❌ Operation cancelled by user{Colors.END}")
                sys.exit(1)
        
        return url
    except Exception as e:
        raise ValueError(f"Invalid target URL: {e}")


def load_proxy_list(proxy_file):
    """Load and validate proxy list from file"""
    if not os.path.isfile(proxy_file):
        raise FileNotFoundError(f"Proxy file not found: {proxy_file}")
    
    proxies = []
    with open(proxy_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Validate proxy format (IP:PORT or full URL)
            try:
                if '://' not in line:
                    # Assume HTTP if no scheme provided
                    line = f"http://{line}"
                
                parsed = urllib.parse.urlparse(line)
                if parsed.hostname and parsed.port:
                    proxies.append(line)
                else:
                    print(f"{Colors.YELLOW}⚠️  Invalid proxy on line {line_num}: {line}{Colors.END}")
            except Exception:
                print(f"{Colors.YELLOW}⚠️  Invalid proxy on line {line_num}: {line}{Colors.END}")
    
    if not proxies:
        raise ValueError("No valid proxies found in file")
    
    return proxies


def load_payloads(payload_file):
    """Load test payloads from file"""
    if not payload_file or not os.path.isfile(payload_file):
        return [None]  # Single request with no payload
    
    with open(payload_file, 'r') as f:
        payloads = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    return payloads or [None]


def create_session():
    """Create a configured requests session"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'PenTest-Tool/1.0 (Educational)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    return session


def make_request(session, target_url, proxy, payload, custom_headers, method, timeout, logger):
    """Make a single HTTP request with error handling"""
    try:
        # Configure proxy
        proxies = None
        if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
        
        # Prepare request parameters
        request_kwargs = {
            'timeout': timeout,
            'proxies': proxies,
            'headers': custom_headers,
            'allow_redirects': True,
            'verify': False  # For testing environments
        }
        
        # Add payload if provided
        if payload:
            if method.upper() == 'GET':
                # Add as URL parameter
                separator = '&' if '?' in target_url else '?'
                request_kwargs['url'] = f"{target_url}{separator}test={payload}"
            else:
                # Add as POST data
                request_kwargs['data'] = {'payload': payload}
                request_kwargs['url'] = target_url
        else:
            request_kwargs['url'] = target_url
        
        # Make request
        if method.upper() == 'GET':
            response = session.get(**request_kwargs)
        elif method.upper() == 'POST':
            response = session.post(**request_kwargs)
        else:
            response = session.request(method.upper(), **request_kwargs)
        
        # Analyze response
        result = {
            'proxy': proxy or 'Direct',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'content_length': len(response.content),
            'payload': payload,
            'headers': dict(response.headers),
            'success': True
        }
        
        # Check for interesting responses
        interesting_patterns = [
            'error', 'exception', 'debug', 'sql', 'mysql', 'oracle',
            'admin', 'root', 'config', 'password', 'unauthorized'
        ]
        
        response_text = response.text.lower()
        found_patterns = [pattern for pattern in interesting_patterns if pattern in response_text]
        if found_patterns:
            result['interesting_patterns'] = found_patterns
        
        # Log successful request
        status_color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
        proxy_info = f"via {proxy}" if proxy else "direct"
        logger.info(f"{status_color}✅ {response.status_code}{Colors.END} | "
                   f"{result['response_time']:.2f}s | "
                   f"{result['content_length']} bytes | "
                   f"{proxy_info}")
        
        if found_patterns:
            logger.warning(f"{Colors.YELLOW}🔍 Interesting patterns found: {', '.join(found_patterns)}{Colors.END}")
        
        return result
        
    except requests.exceptions.ConnectTimeout:
        logger.error(f"{Colors.RED}⏱️ Timeout: {proxy or 'Direct connection'}{Colors.END}")
        return {'proxy': proxy, 'error': 'timeout', 'success': False}
    
    except requests.exceptions.ProxyError:
        logger.error(f"{Colors.RED}🚫 Proxy error: {proxy}{Colors.END}")
        return {'proxy': proxy, 'error': 'proxy_error', 'success': False}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"{Colors.RED}❌ Request failed via {proxy or 'direct'}: {str(e)[:100]}{Colors.END}")
        return {'proxy': proxy, 'error': str(e), 'success': False}


def run_testing_campaign(proxies, target_url, payloads, config, logger):
    """Run the main testing campaign"""
    session = create_session()
    results = []
    total_requests = len(proxies) * len(payloads) if config['use_all_proxies'] else len(payloads)
    completed_requests = 0
    
    print(f"\n{Colors.BLUE}🚀 Starting testing campaign...{Colors.END}")
    print(f"{Colors.CYAN}Target: {target_url}{Colors.END}")
    print(f"{Colors.CYAN}Proxies: {len(proxies)} loaded{Colors.END}")
    print(f"{Colors.CYAN}Payloads: {len(payloads)} loaded{Colors.END}")
    print(f"{Colors.CYAN}Total requests: {total_requests}{Colors.END}")
    print(f"{Colors.BOLD}{'─' * 60}{Colors.END}")
    
    # Choose proxy strategy
    if config['use_all_proxies']:
        proxy_cycle = proxies
    else:
        proxy_cycle = cycle(proxies)
    
    # Execute requests
    for payload in payloads:
        if config['use_all_proxies']:
            # Test with all proxies for this payload
            for proxy in proxy_cycle:
                result = make_request(
                    session, target_url, proxy, payload,
                    config['custom_headers'], config['method'],
                    config['timeout'], logger
                )
                results.append(result)
                completed_requests += 1
                
                # Rate limiting
                if config['delay'] > 0:
                    time.sleep(config['delay'])
        else:
            # Cycle through proxies
            proxy = next(proxy_cycle)
            result = make_request(
                session, target_url, proxy, payload,
                config['custom_headers'], config['method'],
                config['timeout'], logger
            )
            results.append(result)
            completed_requests += 1
            
            # Rate limiting
            if config['delay'] > 0:
                time.sleep(config['delay'])
        
        # Progress update
        if completed_requests % 10 == 0:
            progress = (completed_requests / total_requests) * 100
            print(f"{Colors.CYAN}Progress: {completed_requests}/{total_requests} ({progress:.1f}%){Colors.END}")
    
    return results


def generate_report(results, output_file):
    """Generate detailed test report"""
    if not results:
        print(f"{Colors.YELLOW}⚠️ No results to report{Colors.END}")
        return
    
    # Calculate statistics
    successful_requests = [r for r in results if r.get('success', False)]
    failed_requests = [r for r in results if not r.get('success', False)]
    
    status_codes = {}
    response_times = []
    interesting_findings = []
    
    for result in successful_requests:
        # Status code distribution
        status = result.get('status_code', 0)
        status_codes[status] = status_codes.get(status, 0) + 1
        
        # Response times
        if 'response_time' in result:
            response_times.append(result['response_time'])
        
        # Interesting patterns
        if 'interesting_patterns' in result:
            interesting_findings.append({
                'proxy': result['proxy'],
                'payload': result['payload'],
                'patterns': result['interesting_patterns'],
                'status_code': result['status_code']
            })
    
    # Generate report
    report = {
        'summary': {
            'total_requests': len(results),
            'successful_requests': len(successful_requests),
            'failed_requests': len(failed_requests),
            'success_rate': len(successful_requests) / len(results) * 100 if results else 0
        },
        'status_codes': status_codes,
        'performance': {
            'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0
        },
        'interesting_findings': interesting_findings,
        'detailed_results': results
    }
    
    # Display summary
    print(f"\n{Colors.BOLD}📊 Test Results Summary{Colors.END}")
    print(f"{Colors.BOLD}{'─' * 40}{Colors.END}")
    print(f"Total requests:      {Colors.CYAN}{report['summary']['total_requests']:,}{Colors.END}")
    print(f"Successful:          {Colors.GREEN}{report['summary']['successful_requests']:,}{Colors.END}")
    print(f"Failed:              {Colors.RED}{report['summary']['failed_requests']:,}{Colors.END}")
    print(f"Success rate:        {Colors.YELLOW}{report['summary']['success_rate']:.1f}%{Colors.END}")
    
    if response_times:
        print(f"\nAvg response time:   {Colors.CYAN}{report['performance']['avg_response_time']:.2f}s{Colors.END}")
    
    if status_codes:
        print(f"\n{Colors.BOLD}Status Code Distribution:{Colors.END}")
        for code, count in sorted(status_codes.items()):
            color = Colors.GREEN if code == 200 else Colors.YELLOW if code < 400 else Colors.RED
            print(f"  {color}{code}: {count:,} requests{Colors.END}")
    
    if interesting_findings:
        print(f"\n{Colors.BOLD}🔍 Interesting Findings:{Colors.END}")
        for finding in interesting_findings[:10]:  # Show top 10
            print(f"  {Colors.YELLOW}• Proxy: {finding['proxy']}{Colors.END}")
            print(f"    Patterns: {', '.join(finding['patterns'])}")
            if finding['payload']:
                print(f"    Payload: {finding['payload']}")
    
    # Save detailed report
    if output_file:
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n{Colors.GREEN}✅ Detailed report saved to: {output_file}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error saving report: {e}{Colors.END}")


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog='pentest-tool',
        description='🔐 PenTest Request Tool - Educational Security Testing',
        epilog=f"""
{Colors.BOLD}Basic Usage:{Colors.END}
  {Colors.CYAN}pentest-tool --url http://target.thm --proxy-list proxies.txt{Colors.END}
  {Colors.CYAN}pentest-tool --url http://10.10.10.1 --proxy-list proxies.txt --payloads sqli.txt{Colors.END}

{Colors.BOLD}Advanced Testing:{Colors.END}
  {Colors.CYAN}pentest-tool --url http://target.local/login --proxy-list proxies.txt \\{Colors.END}
  {Colors.CYAN}             --method POST --delay 2 --timeout 10 --output report.json{Colors.END}

{Colors.YELLOW}⚠️  Remember: Only test systems you own or have explicit permission to test!{Colors.END}
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        '--url',
        required=True,
        help='Target URL to test'
    )
    
    parser.add_argument(
        '--proxy-list',
        required=True,
        help='File containing proxy list (IP:PORT or full URLs, one per line)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--payloads',
        help='File containing test payloads (one per line)'
    )
    
    parser.add_argument(
        '--method',
        choices=['GET', 'POST', 'PUT', 'DELETE'],
        default='GET',
        help='HTTP method to use (default: GET)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=1,
        help='Number of concurrent threads (default: 1)'
    )
    
    parser.add_argument(
        '--use-all-proxies',
        action='store_true',
        help='Test each payload with all proxies (instead of cycling)'
    )
    
    parser.add_argument(
        '--custom-header',
        action='append',
        help='Custom header in format "Name: Value" (can be used multiple times)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for detailed JSON report'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        help='Log file path (default: console only)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress banner and minimize output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'{Colors.CYAN}PenTest Request Tool v1.0{Colors.END} - Educational Security Testing'
    )
    
    return parser


def main():
    """Main application entry point"""
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        # Setup logging
        logger = setup_logging(args.log_level, args.log_file)
        
        # Display banner unless in quiet mode
        if not args.quiet:
            print_banner()
        
        # Validate target URL
        target_url = validate_target_url(args.url)
        
        # Load proxy list
        try:
            proxies = load_proxy_list(args.proxy_list)
            logger.info(f"{Colors.GREEN}✅ Loaded {len(proxies)} proxies{Colors.END}")
        except Exception as e:
            logger.error(f"{Colors.RED}❌ Error loading proxies: {e}{Colors.END}")
            sys.exit(1)
        
        # Load payloads
        payloads = load_payloads(args.payloads)
        if args.payloads:
            logger.info(f"{Colors.GREEN}✅ Loaded {len(payloads)} payloads{Colors.END}")
        
        # Parse custom headers
        custom_headers = {}
        if args.custom_header:
            for header in args.custom_header:
                if ':' in header:
                    name, value = header.split(':', 1)
                    custom_headers[name.strip()] = value.strip()
        
        # Configure testing parameters
        config = {
            'method': args.method,
            'delay': args.delay,
            'timeout': args.timeout,
            'use_all_proxies': args.use_all_proxies,
            'custom_headers': custom_headers
        }
        
        # Run testing campaign
        results = run_testing_campaign(proxies, target_url, payloads, config, logger)
        
        # Generate report
        generate_report(results, args.output)
        
        print(f"\n{Colors.GREEN}✅ Testing campaign completed{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Operation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Critical error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()
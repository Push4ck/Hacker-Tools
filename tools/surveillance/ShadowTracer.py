#!/usr/bin/env python3
"""
ShadowTracer - Professional Request Interceptor
Tor-enabled web request interception and analysis tool.
"""

import os
import sys
import json
import time
import random
import subprocess
import argparse
import signal
import threading
from datetime import datetime
from typing import List, Dict, Optional, Any


# Check for required dependencies
try:
    from fake_useragent import UserAgent
    from seleniumwire import webdriver
    from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install required packages with:")
    print("pip install selenium-wire fake-useragent selenium")
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
 ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗████████╗██████╗  █████╗  ██████╗███████╗██████╗ 
 ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
 ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║   ██║   ██████╔╝███████║██║     █████╗  ██████╔╝
 ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║   ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ██╔══██╗
 ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝   ██║   ██║  ██║██║  ██║╚██████╗███████╗██║  ██║
 ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BLUE}    Professional Web Request Interceptor v2.0{Colors.ENDC}
{Colors.CYAN}    Tor-Enabled • Stealth Mode • Advanced Analysis{Colors.ENDC}
    {'─' * 85}
"""
    print(banner)


class TorManager:
    """Manage Tor process lifecycle"""
    
    def __init__(self, port: int = 8088):
        self.port = port
        self.process = None
        self.is_running = False
    
    def start(self, verbose: bool = False) -> bool:
        """Start Tor process"""
        try:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Starting Tor on port {self.port}...")
            
            # Check if Tor is available
            tor_check = subprocess.run(['tor', '--version'], 
                                     capture_output=True, text=True)
            if tor_check.returncode != 0:
                raise FileNotFoundError("Tor not found")
            
            # Start Tor with custom configuration
            self.process = subprocess.Popen([
                'tor',
                '--HTTPTunnelPort', str(self.port),
                '--quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for Tor to initialize
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Waiting for Tor to initialize...")
            
            time.sleep(8)  # Give Tor time to establish circuits
            
            # Verify Tor is running
            if self.process.poll() is None:
                self.is_running = True
                if verbose:
                    print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Tor started successfully")
                return True
            else:
                raise Exception("Tor process terminated unexpectedly")
                
        except FileNotFoundError:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Tor is not installed or not in PATH")
            print("Install Tor: https://www.torproject.org/download/")
            return False
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to start Tor: {str(e)}")
            return False
    
    def stop(self, verbose: bool = False):
        """Stop Tor process"""
        if self.process and self.is_running:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Stopping Tor...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.is_running = False


class BrowserManager:
    """Manage Firefox browser with Tor proxy"""
    
    def __init__(self, proxy_port: int = 8088):
        self.proxy_port = proxy_port
        self.driver = None
        self.user_agent = None
    
    def create_driver(self, headless: bool = True, driver_path: Optional[str] = None, 
                     verbose: bool = False) -> webdriver.Firefox:
        """Create Firefox driver with Tor proxy and stealth settings"""
        try:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Configuring Firefox with Tor proxy...")
            
            # Generate random user agent
            ua = UserAgent()
            self.user_agent = ua.random
            
            # Configure Firefox profile
            profile = FirefoxProfile()
            
            # Privacy and stealth settings
            profile.set_preference('permissions.default.image', 2)  # Block images
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            profile.set_preference('general.useragent.override', self.user_agent)
            profile.set_preference('privacy.privatebrowsing.autostart', True)
            profile.set_preference('network.cookie.cookieBehavior', 1)  # Block third-party cookies
            profile.set_preference('geo.enabled', False)  # Disable geolocation
            profile.set_preference('dom.webnotifications.enabled', False)  # Disable notifications
            profile.set_preference('media.navigator.enabled', False)  # Disable WebRTC
            profile.update_preferences()
            
            # Firefox options
            options = Options()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Selenium Wire options for proxy
            wire_options = {
                'proxy': {
                    'http': f'http://localhost:{self.proxy_port}',
                    'https': f'https://localhost:{self.proxy_port}',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            
            # Create driver
            if driver_path:
                self.driver = webdriver.Firefox(
                    seleniumwire_options=wire_options,
                    firefox_profile=profile,
                    options=options,
                    executable_path=driver_path
                )
            else:
                self.driver = webdriver.Firefox(
                    seleniumwire_options=wire_options,
                    firefox_profile=profile,
                    options=options
                )
            
            # Set random window size for stealth
            if not headless:
                width = random.randint(1024, 1920)
                height = random.randint(768, 1080)
                self.driver.set_window_size(width, height)
                self.driver.set_window_position(random.randint(0, 100), random.randint(0, 100))
            
            if verbose:
                print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Firefox configured successfully")
                print(f"{Colors.CYAN}[INFO]{Colors.ENDC} User Agent: {self.user_agent[:60]}...")
            
            return self.driver
            
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to create Firefox driver: {str(e)}")
            if "geckodriver" in str(e).lower():
                print("Download geckodriver: https://github.com/mozilla/geckodriver/releases")
            raise
    
    def close(self, verbose: bool = False):
        """Close browser driver"""
        if self.driver:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Closing browser...")
            try:
                self.driver.quit()
            except Exception as e:
                if verbose:
                    print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Error closing browser: {str(e)}")


class RequestInterceptor:
    """Intercept and analyze web requests"""
    
    def __init__(self, driver: webdriver.Firefox):
        self.driver = driver
        self.intercepted_requests = []
    
    def navigate_to_url(self, url: str, timeout: int = 30, verbose: bool = False) -> bool:
        """Navigate to target URL"""
        try:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Navigating to: {url}")
            
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            if verbose:
                print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Page loaded successfully")
                print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Title: {self.driver.title}")
            
            return True
            
        except TimeoutException:
            print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Page load timeout after {timeout}s")
            return False
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to navigate: {str(e)}")
            return False
    
    def click_element(self, css_selector: str, timeout: int = 10, verbose: bool = False) -> bool:
        """Click element by CSS selector"""
        try:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Looking for element: {css_selector}")
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # Click element
            element.click()
            
            if verbose:
                print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Element clicked successfully")
            
            return True
            
        except TimeoutException:
            print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Element not found or not clickable: {css_selector}")
            return False
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to click element: {str(e)}")
            return False
    
    def capture_requests(self, match_pattern: str, verbose: bool = False) -> List[Dict[str, Any]]:
        """Capture and filter requests matching pattern"""
        matched_requests = []
        
        if verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Analyzing {len(self.driver.requests)} requests...")
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Looking for pattern: {match_pattern}")
        
        for request in self.driver.requests:
            if match_pattern.lower() in request.url.lower():
                try:
                    # Decode request body
                    payload = None
                    if request.body:
                        try:
                            payload = request.body.decode('utf-8')
                            # Try to parse as JSON if possible
                            try:
                                payload = json.loads(payload)
                            except json.JSONDecodeError:
                                pass  # Keep as string
                        except UnicodeDecodeError:
                            payload = f"<Binary data: {len(request.body)} bytes>"
                    
                    # Extract response info if available
                    response_info = None
                    if request.response:
                        response_info = {
                            'status_code': request.response.status_code,
                            'headers': dict(request.response.headers),
                            'body_size': len(request.response.body) if request.response.body else 0
                        }
                    
                    request_data = {
                        'timestamp': datetime.now().isoformat(),
                        'method': request.method,
                        'url': request.url,
                        'headers': dict(request.headers),
                        'payload': payload,
                        'response': response_info
                    }
                    
                    matched_requests.append(request_data)
                    
                    if verbose:
                        print(f"{Colors.GREEN}[MATCH]{Colors.ENDC} {request.method} {request.url}")
                
                except Exception as e:
                    if verbose:
                        print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Failed to process request: {str(e)}")
        
        return matched_requests
    
    def display_results(self, requests: List[Dict[str, Any]]):
        """Display captured requests in formatted output"""
        if not requests:
            print(f"\n{Colors.YELLOW}[WARNING]{Colors.ENDC} No matching requests found.")
            return
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}🕵️ INTERCEPTED REQUESTS ({len(requests)} found){Colors.ENDC}")
        print("═" * 90)
        
        for i, req in enumerate(requests, 1):
            print(f"\n{Colors.CYAN}{Colors.BOLD}[REQUEST #{i}]{Colors.ENDC}")
            print("─" * 50)
            print(f"{Colors.BOLD}Method:{Colors.ENDC} {req['method']}")
            print(f"{Colors.BOLD}URL:{Colors.ENDC} {req['url']}")
            print(f"{Colors.BOLD}Timestamp:{Colors.ENDC} {req['timestamp']}")
            
            # Headers
            if req['headers']:
                print(f"\n{Colors.BOLD}Headers:{Colors.ENDC}")
                for key, value in list(req['headers'].items())[:5]:  # Show first 5 headers
                    print(f"  {Colors.BLUE}{key}:{Colors.ENDC} {str(value)[:60]}{'...' if len(str(value)) > 60 else ''}")
                if len(req['headers']) > 5:
                    print(f"  {Colors.YELLOW}... and {len(req['headers']) - 5} more headers{Colors.ENDC}")
            
            # Payload
            if req['payload']:
                print(f"\n{Colors.BOLD}Payload:{Colors.ENDC}")
                if isinstance(req['payload'], dict):
                    print(json.dumps(req['payload'], indent=2)[:500])
                else:
                    payload_str = str(req['payload'])[:500]
                    print(payload_str)
                if len(str(req['payload'])) > 500:
                    print(f"{Colors.YELLOW}... (truncated){Colors.ENDC}")
            
            # Response info
            if req['response']:
                resp = req['response']
                print(f"\n{Colors.BOLD}Response:{Colors.ENDC}")
                status_color = Colors.GREEN if 200 <= resp['status_code'] < 300 else Colors.RED
                print(f"  Status: {status_color}{resp['status_code']}{Colors.ENDC}")
                print(f"  Body Size: {resp['body_size']} bytes")
        
        print("\n═" * 90)
    
    def save_results(self, requests: List[Dict[str, Any]], output_file: str):
        """Save results to JSON file"""
        try:
            output_data = {
                'timestamp': datetime.now().isoformat(),
                'total_requests': len(requests),
                'requests': requests
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Results saved to: {output_file}")
            
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Failed to save results: {str(e)}")


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='ShadowTracer',
        description='Professional web request interceptor with Tor anonymization',
        epilog='''
Examples:
  %(prog)s https://example.com api                       # Basic interception
  %(prog)s https://site.com login --click "#login-btn"   # Click element and capture
  %(prog)s https://site.com api --output results.json    # Save results to file
  %(prog)s https://site.com api --visible --verbose      # Visible browser with verbose output
  %(prog)s https://site.com api --timeout 60 --wait 10   # Custom timeouts

Features:
  • Tor proxy for anonymization
  • Random user agents for stealth
  • Request/response analysis
  • Element interaction capabilities
  • JSON output format
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'url',
        help='Target URL to load and analyze'
    )
    
    parser.add_argument(
        'match_pattern',
        help='Pattern to match in request URLs (case-insensitive)'
    )
    
    parser.add_argument(
        '--click',
        metavar='SELECTOR',
        help='CSS selector for element to click before capturing requests'
    )
    
    parser.add_argument(
        '--driver',
        metavar='PATH',
        help='Path to geckodriver executable (auto-detected if not specified)'
    )
    
    parser.add_argument(
        '--output',
        metavar='FILE',
        help='Save results to JSON file'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        metavar='SEC',
        help='Page load timeout in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--wait',
        type=int,
        default=5,
        metavar='SEC',
        help='Wait time after actions before capturing (default: 5)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8088,
        metavar='PORT',
        help='Tor proxy port (default: 8088)'
    )
    
    parser.add_argument(
        '--visible',
        action='store_true',
        help='Run browser in visible mode (not headless)'
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


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.ENDC} Shutting down gracefully...")
    sys.exit(0)


def main():
    """Main application entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = create_parser()
    args = parser.parse_args()
    
    # Display banner unless suppressed
    if not args.no_banner:
        print_banner()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} URL must start with http:// or https://")
        sys.exit(1)
    
    # Initialize components
    tor_manager = TorManager(port=args.port)
    browser_manager = BrowserManager(proxy_port=args.port)
    
    try:
        # Start Tor
        if not tor_manager.start(verbose=args.verbose):
            sys.exit(1)
        
        # Create browser driver
        driver = browser_manager.create_driver(
            headless=not args.visible,
            driver_path=args.driver,
            verbose=args.verbose
        )
        
        # Initialize request interceptor
        interceptor = RequestInterceptor(driver)
        
        # Navigate to target URL
        if not interceptor.navigate_to_url(args.url, timeout=args.timeout, verbose=args.verbose):
            print(f"{Colors.YELLOW}[WARNING]{Colors.ENDC} Continuing despite navigation issues...")
        
        # Click element if specified
        if args.click:
            interceptor.click_element(args.click, verbose=args.verbose)
        
        # Wait for additional requests
        if args.verbose:
            print(f"{Colors.BLUE}[INFO]{Colors.ENDC} Waiting {args.wait}s for additional requests...")
        time.sleep(args.wait)
        
        # Capture and analyze requests
        requests = interceptor.capture_requests(args.match_pattern, verbose=args.verbose)
        
        # Display results
        interceptor.display_results(requests)
        
        # Save results if requested
        if args.output:
            interceptor.save_results(requests, args.output)
        
        if args.verbose:
            print(f"\n{Colors.GREEN}[SUCCESS]{Colors.ENDC} Analysis completed successfully")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.ENDC} Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.ENDC} {str(e)}")
        sys.exit(1)
    
    finally:
        # Cleanup
        browser_manager.close(verbose=args.verbose)
        tor_manager.stop(verbose=args.verbose)


if __name__ == "__main__":
    main()
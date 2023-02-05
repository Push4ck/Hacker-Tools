import requests
import logging
from itertools import cycle
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# List of IP addresses to cycle through
ip_list = ['1.1.1.1', '2.2.2.2', '3.3.3.3']

# Loop through the IP addresses
for ip in cycle(ip_list):
    proxies = {'http': f'http://{ip}', 'https': f'https://{ip}'}

    # Check if the IP address is already in the proxy list
    if not check_ip_reputation(ip):
        logger.warning(f'[-] {ip} is a known proxy or malicious IP address. Skipping.')
        continue

    # Try to get the response from the website
    retries = 0
    max_retries = 3
    while retries < max_retries:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
            response = requests.get('http://example.com', proxies=proxies, headers=headers, timeout=5)
            logger.info(f'[+] {ip} returned status code: {response.status_code}')
            
            # If the status code is 200 (OK), then break the loop
            if response.status_code == 200:
                break
            
        except requests.exceptions.ConnectTimeout as e:
            logger.error(f'[-] {ip} request timed out: {e}')
            time.sleep(5)
        except requests.exceptions.ProxyError as e:
            logger.error(f'[-] {ip} proxy error: {e}')
            pass
        except requests.exceptions.RequestException as e:
            logger.error(f'[-] {ip} request failed: {e}')
            pass
        
        # Sleep for 1 second before retrying
        time.sleep(1)
        retries += 1
    
def check_ip_reputation(ip):
    # You can implement the code to check the reputation of the IP address here
    # For example, you can use a service such as MaxMind or VirusTotal to check the reputation of the IP
    # For the sake of this example, I'll simply return True
    return True

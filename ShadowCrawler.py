import os import sys import json import time import random import subprocess import argparse from fake_useragent import UserAgent from seleniumwire import webdriver from selenium.common.exceptions import NoSuchElementException, WebDriverException from selenium.webdriver import Firefox from selenium.webdriver.firefox.options import Options from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def start_tor(port): try: return subprocess.Popen(["tor", f"--HTTPTunnelPort", f"{port}"]) except FileNotFoundError: print("[!] Tor is not installed or not in PATH.") sys.exit(1)

def build_firefox(user_agent, proxy_port, headless=True): profile = FirefoxProfile() profile.set_preference('permissions.default.image', 2) profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false') profile.set_preference("general.useragent.override", user_agent) profile.set_preference("driver.privatebrowsing.autostart", True) profile.update_preferences()

options = Options()
options.headless = headless

wire_options = {
    'proxy': {
        'http': f'http://localhost:{proxy_port}',
        'https': f'https://localhost:{proxy_port}',
        'no_proxy': ''
    }
}

return webdriver.Firefox(
    seleniumwire_options=wire_options,
    firefox_profile=profile,
    options=options
)

def capture_requests(driver, match_url): for request in driver.requests: if match_url in request.url: try: payload = request.body.decode() if request.body else None print("[+] Match found:") print(json.dumps({ "url": request.url, "headers": dict(request.headers), "payload": payload }, indent=4)) return except Exception as e: print(f"[!] Failed to decode request payload: {e}")

def run_capture(url, match_url, element_css=None, geckodriver_path=None): port = 8088 ua = UserAgent().random tor_proc = start_tor(port) time.sleep(5)

try:
    driver = build_firefox(ua, port)
    driver.set_window_position(0, 0)
    driver.set_window_size(random.randint(1024, 1920), random.randint(800, 1080))
    driver.get(url)

    if element_css:
        try:
            button = driver.find_element("css selector", element_css)
            button.click()
        except NoSuchElementException:
            print("[!] Element not found:", element_css)

    capture_requests(driver, match_url)

except WebDriverException as e:
    print(f"[!] WebDriver error: {e}")
finally:
    driver.quit()
    tor_proc.terminate()

if name == 'main': parser = argparse.ArgumentParser(description="Intercept requests through Tor-enabled Firefox") parser.add_argument("url", help="Target URL to load") parser.add_argument("match_url", help="Part of URL to match in outgoing requests") parser.add_argument("--click", help="CSS selector for element to click", default=None) parser.add_argument("--driver", help="Path to geckodriver executable", default=None) parser.add_argument("--headless", help="Run Firefox in headless mode", action="store_true")

args = parser.parse_args()

run_capture(args.url, args.match_url, args.click, args.driver)


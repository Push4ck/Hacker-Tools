import os
import random
import subprocess
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from seleniumwire import webdriver

# Define the options for seleniumwire
options_wire = {
    'proxy': {
        # The HTTP proxy to use
        'http': 'http://localhost:8088',
        # The HTTPS proxy to use
        'https': 'https://localhost:8088',
        # The addresses of hosts to bypass the proxy for
        'no_proxy': ''
    }
}

def firefox_init():
    # Creates an instance of the UserAgent class
    ua = UserAgent()
    # Generates a random user agent string
    user_agent = ua.random
    try:
        # Launches the Tor process with specific options
        tor_process = subprocess.Popen(["tor", "--HTTPTunnelPort", "8088"])
    except FileNotFoundError:
        # Prints an error message if the Tor executable cannot be found
        print("Error: Tor executable not found. Please ensure that Tor is installed on your system.")
        return None, None
    # Returns the launched Tor process and the generated user agent
    return tor_process, user_agent


def profile_firefox(user_agent):
    # Creates an instance of the FirefoxProfile class
    profile = FirefoxProfile()
    # Disables the automatic loading of images
    profile.set_preference('permissions.default.image', 2)
    # Disables Flash player plugin
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # Overrides the default user agent with the given user agent
    profile.set_preference("general.useragent.override", user_agent)
    # Sets the private browsing mode to start automatically
    profile.set_preference("driver.privatebrowsing.autostart", True)
    # Updates the preferences for the profile
    profile.update_preferences()
    # Returns the created profile
    return profile

def options_firefox():
    # Creates an instance of the FirefoxOptions class
    options = Options()
    # Sets the headless mode to False
    options.headless = False
    # Returns the created options
    return options

def firefox_closing(driver, tor_process):
    # Terminates the tor process if it exists
    if tor_process:
        tor_process.terminate()
        # Quits the Firefox driver if it exists
    if driver:
        driver.quit()

def headless(url, gecko_driver_path=None):
    # Initialize firefox and get tor process and user agent
    tor_process, user_agent = firefox_init()
    # If tor process or user agent is not available, return
    if not tor_process or not user_agent:
        return

    # Loop through 10 times to try to connect
    for x in range(0, 10):
        # Create firefox profile with user agent
        profile = profile_firefox(user_agent)
        # Get firefox options
        options = options_firefox()
        try:
            # Initialize firefox web driver with selenium wire options, firefox profile, options and gecko driver path
            driver = webdriver.Firefox(
                seleniumwire_options=options_wire,
                firefox_profile=profile,
                options=options,
                executable_path=gecko_driver_path)
        except WebDriverException:
            # If gecko driver not found, print error message and close firefox
            print("Error: GeckoDriver not found. Please ensure that GeckoDriver is installed and its path is correct.")
            firefox_closing(None, tor_process)
            return

        # Set window position and size
        driver.set_window_position(0, 0)
        driver.set_window_size(random.randint(1024, 2060), random.randint(1024, 4100))
        # Get the URL
        driver.get(url)
        try:
            # Try to find the element with CSS selector "#<element_id> button"
            button = driver.find_element_by_css_selector("#<element_id> button")
            # If button is found, click it
            if button:
                button.click()
            # Loop through all requests
            for request in driver.requests:
                # If the request path is "https://api.*********.***/*******/*********"
                if request.path == "https://api.*********.***/*******/*********":
                    # Get the request and its body
                    request_api = request
                    raw = str(request_api.body)
                    request_api = raw.split(('b''))
                    payload_raw = request_api[1]
                    payload = payload_raw[:-1]
                    # If payload is available, get the header and payload and print it
                    if payload:
                        header = request.headers
                        print(header, payload)
                        break
                else:
                    continue
            break
        except NoSuchElementException as e:
            # If element not found, print error message
            print("Element not found:", e)
        except Exception as e:
            # If any other error occurred, print error message
            print("Error occurred:", e)
        finally:
            # Close firefox and tor process
            firefox_closing(driver, tor_process)

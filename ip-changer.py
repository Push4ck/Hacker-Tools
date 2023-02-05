import time
from random import randint
from time import sleep
import os
import subprocess
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent



options_wire = {
    'proxy': {
        'http': 'http://localhost:8088',
        'https': 'https://localhost:8088',
        'no_proxy': ''
    }
}

def firefox_init():
    os.system("killall tor")
    time.sleep(1)
    ua = UserAgent()
    user_agent = ua.random
    subprocess.Popen(("tor --HTTPTunnelPort 8088"),shell=True)
    time.sleep(2)
    return user_agent


def profile_firefox():
    profile = FirefoxProfile()
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    profile.set_preference("general.useragent.override", firefox_init())
    profile.set_preference("driver.privatebrowsing.autostart", True)
    profile.update_preferences()
    return profile



def options_firefox():
    options = Options()
    options.headless = False
    return options


def firefox_closing(driver):
    driver.quit()
    time.sleep(3)
    os.system('killall tor')
      


def headless(url):
    for x in range(0, 10):
        profile = profile_firefox()
        options = options_firefox()
        driver = webdriver.Firefox(seleniumwire_options=options_wire,firefox_profile=profile, options=options, executable_path='******/headless_browser/geckodriver')
        driver.set_window_position(0, 0)
        driver.set_window_size(randint(1024, 2060), randint(1024, 4100))
        driver.get(url)
        time.sleep(randint(3,8))
        try:
            if driver.find_element_by_xpath("//*[@id=\"*******\"]/main/div/div/div[1]/div[2]/form/div/div[2]/div[1]/button"):
                driver.find_element_by_xpath("//*[@id=\"*******\"]/main/div/div/div[1]/div[2]/form/div/div[2]/div[1]/button").click()
                time.sleep(randint(3,6))
                for request in driver.requests:
                    if request.path == "https://api.*********.***/*******/*********":
                        request_api = request
                        raw = str(request_api.body)
                        request_api = raw.split(('b\''))
                        payload_raw = request_api[1]
                        payload = payload_raw[:-1]
                        if payload:
                            header = request.headers
                            print(header, payload)
                            break
                else:
                    continue
                break
    
        except:
            firefox_closing(driver)
            time.sleep(5)
        finally:
            firefox_closing(driver)

            
    return header, payload


url="https://check.torproject.org/?lang=fr"
headless(url)
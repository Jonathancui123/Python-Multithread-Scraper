from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

def getDriver():
    # 1. Set up browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=1') # Only log errors
    # Change path to point to your chrome driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
    path = 'C:\\Users\\Jonathan Cui\\AppData\\Local\\ChromeWebdriver\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=os.path.normpath(path), chrome_options=options)
    return driver

def connectPage(browser, URL, signalElemName):
    # 2. Connect to page -- given browser instance and a page number/letter
    attempts = 0
    while attempts < 3:
        # Try 3 times
        try:
            print(f'Connecting...')
            browser.get(URL)
            # Wait until an element is present on the page
            # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, signalElemName)))
            return True
        except:
            # Handle exceptions and retry
            attempts += 1
            print(f'Exception connecting to page {URL}, attempt #{attempts}')
            sleep(1)

    return False


def processPage(URL, outputFile, failed, signalElemName, parser, writer):
    # 3 function to connect all above functions, write to file
    print(f'Processing link {URL}')
    browser = getDriver()
    if connectPage(browser, URL, signalElemName):
        html = browser.page_source
        output = parser(html)
        writer(output, outputFile)
        print('Done')
        ret = True
    else:
        print(f'ERROR: Failed to connect to {URL}')
        failed.append(URL)
        ret = False
    browser.quit()
    return ret



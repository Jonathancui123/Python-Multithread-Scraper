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
    options.add_argument('log-level=3')
    path = 'C:\\Users\\Jonathan Cui\\AppData\\Local\\ChromeWebdriver\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=os.path.normpath(path), chrome_options=options)
    return driver

def connectPage(browser, URL, signalElemName):
    # 2. Connect to page -- given browser instance and a page number/letter
    attempts = 0
    while attempts < 3:
        # Try 3 times
        try:
            browser.get(URL)
            # Wait until an element is present on the page
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, signalElemName)))
            return True
        except:
            # Handle exceptions and retry
            attempts += 1
            print(f'Exception connecting to page {URL}, attempt #{attempts}')
            sleep(1)

    return False

# 3. Write to file given contents and a filename to write to 
def writeToFile(contents, fileName):
    print("writing to file")
    return
 
# 4 function to run on each page, write to files
def processPage(browser, URL, outputFileName, failed, signalElemName, parser):
    if connectPage(browser, URL, signalElemName):
        html = browser.page_source
        output = parser(html)
        writeToFile(output, outputFileName)
    else:
        print(f'ERROR: Failed to connect to {URL}')
        failed.append(URL)




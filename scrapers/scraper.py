from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getDriver():
    # 1. Set up browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless)'
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def connectPage(browser, path, signalElemName):
    # 2. Connect to page -- given browser instance and a page number/letter
    attempts = 0
    while attempts < 3:
        # Try 3 times
        try:
            browser.get(path)
            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, signalElemName)))
            return True
        except:
            # Handle exceptions and retry
            attempts += 1
            print(f'Exception connecting to page {character}, attempt #{attempts}')
            sleep(1)

    print(f'ERROR: Failed to connect to {path}')
    return False


            


# Wait until an element is present on the page
 
# 3. Parse HTML (capture info from each page -- given an html file)




# 4. Write to file given contents and a file to write to 
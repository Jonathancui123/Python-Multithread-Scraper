from selenium import webdriver
import os
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
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
            # print(f'Connecting...')
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

class WriterThread(ThreadPoolExecutor):
    '''
    Limit file writing to a single thread to avoid data corruption/write errors due to GIL
    Custom writer thread based on the ThreadPoolExecutor
    '''
    def __init__(self):
        print("Initializing writer")
        ThreadPoolExecutor.__init__(self, max_workers=1)
        self.count = 0
        print("Initialized")

    def writeTxt(self, lines, fileName):
        return

    def __writeCsv(self, dicts, fileName):
        # print("__writeCsv")
        # print(dicts[0].keys())
        fieldnames = [key for key in dicts[0].keys()]
        # print(f"filename {fileName}")
        with open(fileName, 'a') as file:
            # print("filename open")
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for newDict in dicts:
                writer.writerow(newDict)
            self.count += 1
            print(f'Finished writing job #{self.count}...')

    def writeCsv(self, dicts, fileName):
        # print("recieving print job")
        assert(fileName[-3:] == "csv")
        ''' Takes in iterable of dictionaries, and a csv filename to write to'''
        future = self.submit(self.__writeCsv, dicts, fileName)

writerThread = WriterThread()

def writeAnyFile(contents, fileName):
    if fileName[-3:] == "csv":
        writerThread.writeCsv(contents, fileName)
    elif fileName[-3:] == "txt":
        writerThread.writeTxt(contents, fileName)
    else:
        raise "Invalid file type"

def processPage(URL, failed, signalElemName, parser, fileName):
    # 3 function to connect all above functions, write to file
    print(f'Processing link {URL}')
    browser = getDriver()
    if connectPage(browser, URL, signalElemName):
        html = browser.page_source
        contents = parser(html)
        writeAnyFile(contents, fileName)
        # print('Done')
        ret = True
    else:
        print(f'ERROR: Failed to connect to {URL}')
        failed.append(URL)
        ret = False
    browser.quit()
    return ret


if __name__ == "__main__":

    import os
    import datetime
    from pathlib import Path

    newDict = {
        "Word" : "Grob",
        "Meaning" : "Very much a grobby grob",
        "Example" : "I once met a very nice grob and I liked it very much!"
    }

    def outputCsvPath():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        outputs = dir_path + '\\outputs\\'
        Path(outputs).mkdir(parents=True, exist_ok=True)

        output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        output_filename = f'output_{output_timestamp}.csv'
        return outputs+output_filename

    with WriterThread() as testWriterThread:
        for _ in range(10):
            testWriterThread.writeCsv([newDict], outputCsvPath())
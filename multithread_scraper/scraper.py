import os
import csv
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driverPath = 'C:\\Users\\Jonathan Cui\\AppData\\Local\\ChromeWebdriver\\chromedriver.exe'

def getDriver():
    '''Set up browser'''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=1') # Only log errors
    # Change path to point to your chrome driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
    driver = webdriver.Chrome(executable_path=os.path.normpath(driverPath), chrome_options=options)
    return driver

def connectPage(browser, URL, signalElemName):
    '''Connect to page -- given browser instance and a page number/letter'''
    attempts = 0
    while attempts < 3:
        # Try 3 times
        try:
            browser.get(URL)
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
        self.startTime = time()
        self.count = 0
        print("Initialized")

    def __writeTxt(self, lines, fileName):
        with open(fileName, 'a') as file:
            for row in lines:
                file.write(row + "\n")
            self.count += 1
            elapsed = time() - self.startTime
            print(f'Finished writing job #{self.count}... ({round(elapsed/self.count, 2)}s per job)')

    def writeTxt(self, lines, fileName):
        ''' 
        Takes in iterable of lines, and a text filename to write to
        Submits a task to the writer thread
        '''
        assert(fileName[-3:] == "txt")
        self.submit(self.__writeTxt, lines, fileName)

    def __writeCsv(self, dicts, fileName):
        fieldnames = [key for key in dicts[0].keys()]
        with open(fileName, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for newDict in dicts:
                writer.writerow(newDict)
            self.count += 1
            elapsed = time() - self.startTime
            print(f'Finished writing job #{self.count}... (avg {elapsed/self.count}s per job)')

    def writeCsv(self, dicts, fileName):
        ''' 
        Takes in iterable of dictionaries, and a csv filename to write to
        Submits a task to the writer thread
        '''
        assert(fileName[-3:] == "csv")
        self.submit(self.__writeCsv, dicts, fileName)

#Export writer thread instance
writerThread = WriterThread()

def writeAnyFile(contents, fileName):
    '''Chooses which file writing method to use'''
    if fileName[-3:] == "csv":
        writerThread.writeCsv(contents, fileName)
    elif fileName[-3:] == "txt":
        writerThread.writeTxt(contents, fileName)
    else:
        raise "Invalid file type"

def processPage(URL, failed, signalElemName, parser, fileName):
    '''Function to connect all above functions, write to file'''
    print(f'Processing link {URL}')
    browser = getDriver()
    if connectPage(browser, URL, signalElemName):
        html = browser.page_source
        contents = parser(html)
        writeAnyFile(contents, fileName)
        ret = True
    else:
        print(f'ERROR: Failed to connect to {URL}')
        failed.append(URL)
        ret = False
    browser.quit()
    return ret
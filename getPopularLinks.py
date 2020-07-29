import datetime
import string
from time import sleep, time
from bs4 import BeautifulSoup
from scraper import getDriver, processPage
from pathlib import Path

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
popularLinks = dir_path + '\\outputs\\popularLinks\\'

#Track elapsesd time throughout the project

# 3. Parse HTML (capture info from each page -- given an html file)
# Return a list of content

popularURL = "https://www.urbandictionary.com/popular.php?character="
urbanDictionaryURL = "https://www.urbandictionary.com"

def parseUDPopularHTML(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        focus = soup.find(id="columnist")
        paths = [ a['href'] for a in focus.find_all('a') ]
        outputLinks = map(lambda path: urbanDictionaryURL+path ,paths)
        return outputLinks
    except Exception as e:
        print(f'Error parsing: {e}')


def writeToFile(contents, file):
    for row in contents:
        file.write(row + "\n")


if __name__ == '__main__':
    # 2. Handler script set up browser, to decide which pages to run the function on, track elapsed time, open and close files, 
    browser = getDriver()
    # Put a timestamp on the output file
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.txt'
    # Track elapsed time and failed URLs
    startTime = time()
    failedURLs = []
    
    # Make new folder if needed
    Path(popularLinks).mkdir(parents=True, exist_ok=True)                
    with open(popularLinks + output_filename, 'a') as file:
        for char in string.ascii_uppercase:
            print(f'Processing letter {char}')
            processPage(browser, popularURL + char, file, failedURLs, "columnist", parser=parseUDPopularHTML, writer=writeToFile)
            print(f'Done {char}')
            sleep(3)
    browser.quit()
    endTime = time()
    elapsed_time = endTime - startTime
    print(f'Elapsed time: {elapsed_time}s with the following failures:')
    print(failedURLs)
import datetime
import string
from time import sleep, time
from bs4 import BeautifulSoup
import csv
from pathlib import Path
import os 
from scraper import getDriver, processPage

from getPopularLinks import popularLinks
dir_path = os.path.dirname(os.path.realpath(__file__))
definitions = dir_path + '\\outputs\\definitions\\'

def parseDefinition(html):
    soup = BeautifulSoup(html, 'html.parser')
    defPanel = soup.find(class_="def-panel")
    word = defPanel.find(class_="word").get_text()
    meaning = defPanel.find(class_="meaning").get_text()
    try:
        example = defPanel.find(class_="example").get_text()
    except:
        example = None
    wordDefinition = {
        'word': word,
        'meaning': meaning,
        'example': example
    }
    return wordDefinition

def writeToCsv(dictionary, file):
    fieldnames=['word','meaning','example']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerow(dictionary)


if __name__ == '__main__':
    # 2. Handler script set up browser, to decide which pages to run the function on, track elapsed time, open and close files, 
    browser = getDriver()
    # Put a timestamp on the output file
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    # Track elapsed time and failed URLs
    startTime = time()
    failedURLs = []
    
    # Read the newest file of popular links
    linkFiles = sorted([f for f in os.listdir(popularLinks) if os.path.isfile(os.path.join(popularLinks, f))])
    popularLinksFile = linkFiles[0]
    print(f'Using link file: {popularLinksFile}')

    # Make new folder if needed
    Path(definitions).mkdir(parents=True, exist_ok=True)                
    with open(definitions + output_filename, 'a') as file, open(os.path.join(popularLinks, popularLinksFile), 'r') as sourceFile:
        for link in sourceFile:
            if(len(link) > 0):
                link = link[:-1] #Remove newline character
                print(f'Processing link {link}')
                processPage(browser, link, file, failedURLs, "def-panel", parser=parseDefinition, writer=writeToCsv)
                print(f'Done {link}')
                sleep(3)
    browser.quit()
    endTime = time()
    elapsed_time = endTime - startTime
    print(f'Elapsed time: {elapsed_time}s with the following failures:')
    print(failedURLs)
import datetime
from time import sleep, time
from bs4 import BeautifulSoup
from pathlib import Path
import os 
from multithread_scraper.scraper import getDriver, processPage
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 10

from getPopularLinks import popularLinks
dir_path = os.path.dirname(os.path.realpath(__file__))
definitions = dir_path + '\\outputs\\definitions\\'

def parseDefinition(html):
    ''' Parser must return an iterable for the writer function'''
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
    return [wordDefinition]



if __name__ == '__main__':
    # 2. Handler script to decide which pages to run the function on, track elapsed time, open and close files, 
    # Put a timestamp on the output file
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    # Track elapsed time and failed URLs
    startTime = time()
    failedURLs = []
    
    # Read the newest file of popular links
    linkFiles = sorted([f for f in os.listdir(popularLinks) if os.path.isfile(os.path.join(popularLinks, f))])
    try: 
        popularLinksFile = linkFiles[-1]
    except:
        raise('link file not found')
    print(f'Using link file: {popularLinksFile}')

    # Make new folder if needed
    Path(definitions).mkdir(parents=True, exist_ok=True)                

    with open(os.path.join(popularLinks, popularLinksFile), 'r') as sourceFile:
        numLinks = len(sourceFile.readlines())

    with open(definitions + output_filename, 'a') as file, open(os.path.join(popularLinks, popularLinksFile), 'r') as sourceFile:
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            args = ([link for link in sourceFile], [failedURLs]*numLinks, ["def-panel"]*numLinks, [parseDefinition]*numLinks, [definitions + output_filename]*numLinks )
            print(len(args[0]))
            executor.map(processPage, *args)
    endTime = time()
    elapsed_time = endTime - startTime
    print(f'Elapsed time: {elapsed_time}s with the following failures:')
    print(failedURLs)
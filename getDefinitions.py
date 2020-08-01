import datetime
from time import sleep, time
from pathlib import Path
import os 
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from multithread_scraper.scraper import getDriver, processPage
from multithread_scraper.timeit import timeit
from getPopularLinks import popularLinks

dir_path = os.path.dirname(os.path.realpath(__file__))
definitions = dir_path + '\\outputs\\definitions\\'
MAX_THREADS = 10

def parseDefinition(html):
    ''' Parser reads html and gives definition. (must return an iterable for the writer function)'''
    try:
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
    except Exception as e:
        print(f'Error parsing: {e}')
        return []

@timeit
def getDefinitions():
    '''Handler script to decide which pages to scrape and create folders '''
    # Put a timestamp on the output file
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    
    failedURLs = []
    
    # Read the newest file of popular links
    linkFiles = sorted([f for f in os.listdir(popularLinks) if os.path.isfile(os.path.join(popularLinks, f))])
    try: 
        popularLinksFile = linkFiles[-1]
    except:
        raise('link file not found')
    print(f'Using link file: {popularLinksFile}')
    
    # Count lines in source file for thread job submission
    with open(os.path.join(popularLinks, popularLinksFile), 'r') as sourceFile:
        numLinks = len(sourceFile.readlines())

    # Make new folder if needed
    Path(definitions).mkdir(parents=True, exist_ok=True)                

    with open(os.path.join(popularLinks, popularLinksFile), 'r') as sourceFile, ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Format arguments as iterable for threadpoolexecutor
        args = [[link for link in sourceFile], [failedURLs], ["def-panel"], [parseDefinition], [definitions + output_filename]]
        for i in range(1, len(args)):
            args[i] = args[i] * numLinks

        # Submit jobs to executor
        executor.map(processPage, *args)
    print('Failed URLs:')
    print(failedURLs)

if __name__ == '__main__':
   getDefinitions()
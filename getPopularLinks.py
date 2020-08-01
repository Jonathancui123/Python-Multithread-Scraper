import datetime
import string
import os
from pathlib import Path
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from multithread_scraper.scraper import getDriver, processPage
from multithread_scraper.timeit import timeit

dir_path = os.path.dirname(os.path.realpath(__file__))
popularLinks = dir_path + '\\outputs\\popularLinks\\'
MAX_THREADS = 10

popularURL = "https://www.urbandictionary.com/popular.php?character="
urbanDictionaryURL = "https://www.urbandictionary.com"

def parseUDPopularHTML(html):
    ''' Parser reads html and gives links. Must return an iterable for the writer function'''
    try:
        soup = BeautifulSoup(html, 'html.parser')
        focus = soup.find(id="columnist")
        paths = [ a['href'] for a in focus.find_all('a') ]
        outputLinks = map(lambda path: urbanDictionaryURL+path ,paths)
        return outputLinks
    except Exception as e:
        print(f'Error parsing: {e}')
        return []

@timeit
def getPopularLinks():
    '''Handler script to decide which pages to scrape and create folders '''
    # Put a timestamp on the output file
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.txt'
    
    failedURLs = []
    
    # Make new folder if needed
    Path(popularLinks).mkdir(parents=True, exist_ok=True) 
                   
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Format arguments as iterable for threadpoolexecutor
        count = len(string.ascii_uppercase)
        args = [[popularURL + char for char in string.ascii_uppercase], [failedURLs], ["columnist"], [parseUDPopularHTML], [popularLinks + output_filename]]
        for i in range(1, len(args)):
            args[i] = args[i] * count

        # Submit jobs to executor
        executor.map(processPage, *args)

    print('Failed URLs:')
    print(failedURLs)
    

if __name__ == '__main__':
    getPopularLinks()
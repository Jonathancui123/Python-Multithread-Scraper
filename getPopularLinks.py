import datetime
import string
from time import sleep, time
from bs4 import BeautifulSoup
from scraper import getDriver, processPage

#Track elapsesd time throughout the project

# 3. Parse HTML (capture info from each page -- given an html file)
def parseUDPopularHTML(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.find(id="columnist").prettify())

if __name__ == '__main__':
    # 2. Handler script set up browser, to decide which pages to run the function on, track elapsed time, open and close files, 
    browser = getDriver()
    baseURL = "https://www.urbandictionary.com/popular.php?character="
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    startTime = time()
    failedURLs = []
    for char in string.ascii_uppercase:
        print(f'Processing letter {char}')
        processPage(browser, baseURL + char, output_filename, failedURLs, "columnist", parseUDPopularHTML)
        sleep(2)
    browser.quit()
    endTime = time()
    elapsed_time = endTime - startTime
    print(f'Elapsed time: {elapsed_time} with the following failures:')
    print(failedURLs)
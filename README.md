# Python-Multithread-Scraper 📋
Python-Multithread-Scraper is a project for me to learn about multithreading in python and web scraping with Selenium + BeautifulSoup. Multithreading significantly reduces the work for web scraping because the bulk of the task (waiting for webpage responses) is I/O bound, meaning several pages can be scraped at once.

It scrapes ~3.6k of the most viewed definitions from the popular site UrbanDictionary.com

getPopularLinks.py scrapes links to the most popular words from Urban Dictionary's "most popular words by letter" pages - exports a .txt file

getDefinitions.py scrapes the top definition for each popular word - exports a .csv file with the word, the meaning, and an example in each row

## Installation
Find dependencies in requirements.txt

```bash
pip install requirements.txt
```
Install Chrome Webdriver for selenium: https://chromedriver.chromium.org/downloads and modify the driverPath variable in scraper.py to point to your installation

## Usage

```python
python -m getPopularLinks
python -m getDefinitions
```

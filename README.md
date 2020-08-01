# Python-Multithread-Scraper
Python-Multithread-Scraper is a project for me to learn about multithreading in python and web scraping with Selenium + BeautifulSoup.

This project is set up to scrape ~3.6k of the most viewed definitions from the popular site UrbanDictionary.com

getPopularLinks.py scrapes links to the most popular words from Urban Dictionary's "most popular words by letter" pages - exports a .txt file

getDefinitions.py scrapes the top definition for each popular word - exports a .csv file with the word, the meaning, and an example in each row

## Installation
Find dependencies in requirements.txt

```bash
pip install requirements.txt
```

Note that the path to chromewebdriver.exe is hard coded in scraper.py

## Usage

```python
python -m getPopularLinks
python -m getDefinitions
```

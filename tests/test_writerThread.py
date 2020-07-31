import pytest
import os
import datetime
from pathlib import Path
from multithread_scraper.scraper import writerThread

@pytest.fixture
def genDict():
    newDict = {
        "Word" : "Grob",
        "Meaning" : "Very much a grobby grob",
        "Example" : "I once met a very nice grob and I liked it very much!"
    }
    return newDict

@pytest.fixture
def outputCsvPath():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    outputs = dir_path + '\\outputs\\'
    Path(outputs).mkdir(parents=True, exist_ok=True)

    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    return outputs+output_filename


def test_writerThread(genDict, outputCsvPath):
    dictionary = genDict
    writerThread.writeCsv([dictionary for _ in range(10)], outputCsvPath)
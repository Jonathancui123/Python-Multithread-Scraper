from selenium import webdriver

# 1. Set up browser
def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless)'
    driver = webdriver.Chrome(chrome_options=options)
    return driver

# 2. Connect to page -- given browser instance and a page number/letter
# Try 3 times
# Wait until an element is present on the page
# Handle exceptions and retry
 
# 3. Parse HTML (capture info from each page -- given an html file)



# 4. Write to file given contents and a file to write to 
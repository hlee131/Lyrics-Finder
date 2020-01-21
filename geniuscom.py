from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

options = Options()
options.headless = True
chromepath = r'C:\Users\ha\Desktop\GitHub Projects\Lyrics Finder\chromedriver.exe'
driver = webdriver.Chrome(chromepath, options=options)

def find(searchterm):
    query = searchterm.split()
    query = '%20'.join(query)
    query = 'http://genius.com/search?q=%s' % (query)
    driver.get(query)

    panels = driver.find_element_by_xpath("""/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]""")
    songs = panels.find_elements_by_xpath(""".//div[@class='mini_card-title']""")
    artists = panels.find_elements_by_xpath(""".//div[@class='mini_card-subtitle']""")

    keys = list(range(len(songs)))
    values = []

    for s, a in zip(songs, artists):
        values.append('%s by %s' % (s, a))

    options = {k:v for k,v in zip(keys, values)}

    for key, value in options.items():
        print('%s : %s' % (key, value))
    
find('mind is a prison')
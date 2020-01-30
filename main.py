# We need Selenium because Youtube is loaded with JavaScript
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os 

options = Options()
options.headless = True
chromepath = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(chromepath, options=options)

lyric_source = input('Would you like to use azlyrics.com [1] or genius.com? [2] ')

while lyric_source not in ['1', '2']:
    lyric_source = input('Please use either 1 or 2 to denote your answer. ')


def start():
    if lyric_source == '1':
        from lyricsources import azlyricscom
        search = input('What song would you like to find the lyrics for today? ')
        azlyricscom.find(search)

    elif lyric_source == '2':
        from lyricsources import geniuscom
        search = input('What song would you like to find the lyrics for today? ')
        geniuscom.find(search)

def watch(searchterm):
    search = searchterm.split()
    search = '+'.join(search)
    link = f'https://www.youtube.com/results?search_query={search}'

    driver.get(link)
    watch_at = driver.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a""")
    yt_link = watch_at.get_attribute('href')

    return(yt_link)

if __name__ == '__main__':
    start() 
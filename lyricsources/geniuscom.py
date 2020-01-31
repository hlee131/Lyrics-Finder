# We need Selenium because Genius is loaded with JavaScript
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import sys
import os 

options = Options()
options.headless = True
chromepath = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(chromepath, options=options)


def watch(searchterm):

    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")
    chromepath = os.getcwd() + r'\chromedriver.exe'
    driver = webdriver.Chrome(chromepath, options=options)

    search = searchterm.split()
    search = '+'.join(search)
    link = f'https://www.youtube.com/results?search_query={search}'

    driver.get(link)
    watch_at = driver.find_element_by_xpath("""/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a""")
    yt_link = watch_at.get_attribute('href')

    return(yt_link)

def write():
    # Writes to file
    with open('%s.txt' % (scrape.songname), 'w', encoding='utf-8') as file:
        file.write(scrape.header + '\n')
        file.write('\n' + scrape.lyrics)

def find(searchterm):
    find.searchterm = searchterm
    query = searchterm.split()
    query = '%20'.join(query)
    query = 'http://genius.com/search?q=%s' % (query)
    driver.get(query)

    panels = driver.find_element_by_xpath("""/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]""")
    songs = panels.find_elements_by_xpath(""".//div[@class='mini_card-title']""")
    artists = panels.find_elements_by_xpath(""".//div[@class='mini_card-subtitle']""")
    link = panels.find_elements_by_xpath("""/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div/search-result-item/div/mini-song-card/a""")
    numoptions = len(songs)

    keys = list(range(1, numoptions + 1))
    values = []
    urls = [l.get_attribute("href") for l in link]

    for s, a in zip(songs, artists):
        values.append('%s by %s' % (s.text, a.text))

    options = {k:v for k,v in zip(keys, values)}

    for key, value in options.items():
        print('%s : %s' % (key, value))

    if len(options) == 0:
        answer = input("Sorry, we couldn't find anything for your search term, would you like to try another song[1],\nor quit[2]?")

        if answer == '1':
            start()

        elif answer == '2':
            sys.exit()
    else:
        selection = int(input('Please choose one of the options with a number from 1-%s. ' % (str(numoptions))))

        while selection not in keys:
            selection = int(input('Please choose one of the options with a number from 1-%s.' % (str(numoptions))))

        find.selected = values[int(selection) - 1]

        scrape(urls[int(selection) - 1])
    
def scrape(url=None):
    
    scrape.url = url

    scrape.source = requests.get(scrape.url).text

    soup = BeautifulSoup(scrape.source, 'lxml')

    # Find song name and artist
    scrape.songname = soup.find('h1', class_='header_with_cover_art-primary_info-title').text
    scrape.artist = soup.find('a', class_= 'header_with_cover_art-primary_info-primary_artist').text
    lyrics = soup.find('div', class_= 'lyrics')
    scrape.lyrics = lyrics.find('p').text
    scrape.header = '%s by %s' % (scrape.songname, scrape.artist)
    scrape.valid = True

    scrape.link = watch(find.searchterm)
    scrape.link = f'\n\nWatch now at: {scrape.link}'

    yesno = input('Would you like to write the lyrics to a file? (y/n) ')
    while yesno not in ['y', 'n']:
        yesno = input("Please use either 'y' or 'n' ")

    # Calls write only if user said yes
    if yesno == 'y':
        write()

    # Prints lyrics
    lyrics = scrape.header + scrape.lyrics + scrape.link + '\n'
    print(lyrics)

    scrape.again = input('Would you like to try another song[1] or quit[2]? ')

    while scrape.again not in ['1', '2']:
        scrape.again = input("'%s' is an invalid answer. Please try again. " % (scrape.again))

    if scrape.again == '1':
        start()

    elif scrape.again == '2':
        sys.exit()

def start():
    search = input('What song would you like to find the lyrics for today? ')
    find(search)

if __name__ == '__main__':
    start()

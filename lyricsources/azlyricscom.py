from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import lxml
import requests
import sys
import os

def watch(searchterm):

    options = Options()
    options.headless = True
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
    with open('%s.txt' % (scrape.songname), 'w') as file:
        file.write(scrape.header)
        file.write(scrape.lyrics)
        file.write(scrape.link)

def scrape(url=None):
    
    scrape.url = url

    scrape.source = requests.get(scrape.url).text

    soup = BeautifulSoup(scrape.source, 'lxml')

    # Find song name and artist
    songname = soup.find_all('b')[1].text
    scrape.songname = songname[1:-1]
    artist = soup.find('div', class_='col-xs-12 col-lg-8 text-center').find('div', class_='lyricsh').h2.text
    scrape.artist = artist[:-7]
    scrape.lyrics = soup.find('div', class_=None).text.strip()
    scrape.header = '\n%s by %s \n' % (songname, artist)
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

def find(searchterm):
    find.searchterm = searchterm
    query = searchterm.split()
    queryinlink = '+'.join(query)
    newurl = 'https://search.azlyrics.com/search.php?q=%s' % (queryinlink)
    newsource = requests.get(newurl).text
    newsoup = BeautifulSoup(newsource, 'lxml')
    panels = newsoup.find_all('div', class_='panel')

    if len(panels) > 1:
        ourpanel = panels[len(panels) - 1]

    elif len(panels) == 1:
        ourpanel = panels[0]

    elif len(panels) == 0:
        answer = input("Sorry, we couldn't find anything for your search term, would you like to try another song[1],\nor quit[2]? ")

        if answer == '1':
            start()

        elif answer == '2':
            sys.exit()

    topfive = ourpanel.find_all('td', class_='text-left visitedlyr', limit = 5)
    numoptions = len(topfive)
    
    keys = list(range(1, numoptions + 1))
    values = []
    urls = []
    for song in topfive:
        artist = str(song.a.b.next_element.next_element.next_element)
        values.append('%s by %s' % (song.a.b.text, artist[3:-4]))
        urls.append(song.a['href'])

    options = {k:v for k,v in zip(keys, values)}
    
    for key, value in options.items():
        print('%s : %s' % (key, value))

    
    selection = int(input('Please choose one of the options with a number from 1-%s. ' % (str(numoptions))))

    while selection not in keys:
        selection = int(input('Please choose one of the options with a number from 1-%s.' % (str(numoptions))))

    find.selected = values[int(selection) - 1]

    scrape(urls[int(selection) - 1])

def start():
    search = input('What song would you like to find the lyrics for today? ')
    find(search)

if __name__ == '__main__':
    start() 






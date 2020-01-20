from bs4 import BeautifulSoup
import lxml
import requests
import sys

def write():
    # Writes to file
    with open('%s.txt' % (scrape.songname), 'w') as file:
        file.write(scrape.header)
        file.write(scrape.lyrics)

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

    yesno = input('Would you like to write the lyrics to a file? (y/n) ')
    while yesno not in ['y', 'n']:
        yesno = input("Please use either 'y' or 'n' ")

    # Calls write only if user said yes
    if yesno == 'y':
        write()

    # Prints lyrics
    print(scrape.header)
    print(scrape.lyrics +'\n')

    scrape.again = input('Would you like to try another song[1] or quit[2]? ')

    while scrape.again not in ['1', '2']:
        scrape.again = input("'%s' is an invalid answer. Please try again. " % (scrape.again))

    if scrape.again == '1':
        start()

    elif scrape.again == '2':
        sys.exit()

def find(searchterm):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    query = searchterm.split()
    queryinlink = '%20'.join(query)
    newurl = 'http://genius.com/search?q=%s' % (queryinlink)
    newsource = requests.get(newurl, headers=headers).text
    newsoup = BeautifulSoup(newsource, 'lxml')
    print(newsoup.prettify())
    panels = newsoup.find_all('div', {'ng-switch' : "$ctrl.section.type === 'album' || ($ctrl.section.type === 'top_hit' && $ctrl.section.hits[0].index === 'album')"})
    #print(panels)

    topfive = panels[0].find_all('div', {'ng-repeat' : 'hit in $ctrl.results | limitTo: $ctrl.limit_to'}, limit = 5)

    # print(topfive)
    
    keys = ['1', '2', '3', '4', '5']
    values = []
    urls = []

    for song in topfive:
        song = song.find('div', class_='mini_card-title').text
        artist = song.find('div', class_='mini_card-subtitle').text
        values.append('%s by %s' % (song, artist))
        urls.append(song.find(class_='mini_card')['href'])

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
        selection = input('Please choose one of the options with a number from 1-5. ')

        while selection not in keys:
            selection = input('Please choose one of the options with a number from 1-5.')

        print(urls[int(selection) - 1])

        # scrape(urls[int(selection) - 1])

def start():
    search = input('What song would you like to find the lyrics for today? ')
    find(search)

start()






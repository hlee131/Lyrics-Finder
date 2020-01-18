from bs4 import BeautifulSoup
import lxml
import requests
import sys

def write():
    # Writes to file
    with open('%s.txt' % (search.songname), 'w') as file:
        file.write(search.header)
        file.write(search.lyrics)

def search(url=None):
    
    search.url = url

    search.source = requests.get(search.url).text

    soup = BeautifulSoup(search.source, 'lxml')

    # Find song name and artist
    songname = soup.find_all('b')[1].text
    search.songname = songname[1:-1]
    artist = soup.find('div', class_='col-xs-12 col-lg-8 text-center').find('div', class_='lyricsh').h2.text
    search.artist = artist[:-7]
    search.lyrics = soup.find('div', class_=None).text.strip()
    search.header = '\n%s by %s \n' % (songname, artist)
    search.valid = True

    yesno = input('Would you like to write the lyrics to a file? (y/n) ')
    while yesno not in ['y', 'n']:
        yesno = input("Please use either 'y' or 'n' ")

    # Calls write only if user said yes
    if yesno == 'y':
        write()

    # Prints lyrics
    print(search.header)
    print(search.lyrics +'\n')

    search.again = input('Would you like to try another song[1] or quit[2]? ')

    while search.again not in ['1', '2']:
        search.again = input("'%s' is an invalid answer. Please try again. " % (search.again))

    if search.again == '1':
        start()

    elif search.again == '2':
        sys.exit()

def find(searchterm):
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

    topfive = ourpanel.find_all('td', class_='text-left visitedlyr', limit = 5)
    
    keys = ['1', '2', '3', '4', '5']
    values = []
    urls = []
    for song in topfive:
        artist = str(song.a.b.next_element.next_element.next_element)
        values.append('%s by %s' % (song.a.b.text, artist[3:-4]))
        urls.append(song.a['href'])

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

        search(urls[int(selection) - 1])


def start():
    search = input('What song would you like to find the lyrics for today? ')
    find(search)

start()






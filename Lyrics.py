from bs4 import BeautifulSoup
import lxml
import requests
import sys

def write():
    # Writes to file
    file = open('%s.txt' % (search.songname), 'w')
    file.write(search.header)
    file.write(search.lyrics)
    file.close()

def search():
    
    # Asks for name and artist and opens url
    search.name = input('What is the name of your song? ')
    name = search.name.replace(' ', '').lower()
    name = str(name)
    artist = input('Who is the artist of your song? ').lower()
    artist = artist.replace(' ', '')
    yn = False
    yesno = input("Would you like to print the lyrics to a file? (y/n) ")
    validchar = ['y', 'n']

    #  Validates answer
    while not yn:
        if yesno not in validchar:
            yesno = input("'%s' is an invalid input. Try again. (y/n) " % (yesno)) 

        elif yesno in validchar:
            yn = True

    search.url = 'https://azlyrics.com/lyrics/%s/%s.html' % (artist, name)
    search.source = requests.get(search.url).text

    soup = BeautifulSoup(search.source, 'lxml')

    # Find song name and artist
    try:
        songname = soup.find_all('b')[1].text
        search.songname = songname[1:-1]
        artist = soup.find('div', class_='col-xs-12 col-lg-8 text-center').find('div', class_='lyricsh').h2.text
        search.artist = artist[:-7]
        search.lyrics = soup.find('div', class_=None).text.strip()
        search.header = '\n%s by %s \n' % (songname, artist)
        search.valid = True

        # Calls write only if user said yes
        if yesno == 'y':
            write()

        # Prints lyrics
        print(search.header)
        print(search.lyrics +'\n')

        search.again = input('Would you like to try another song? (y/n) ')
        while search.again not in validchar:
            search.again = input("'%s' is an invalid answer. Please try again. (y/n) " % (search.again))

    except:
        search.valid = False
        search.again = 'n'
        search.songname = search.name
        search.artist = artist
        search.query = "'%s' by '%s'" % (search.songname, search.artist)

def find():
    query = 'this by that'.split()
    queryinlink = '+'.join(query)
    newurl = 'https://search.azlyrics.com/search.php?q=%s' % (queryinlink)
    print(newurl)
    newsource = requests.get(newurl).text
    newsoup = BeautifulSoup(newsource, 'lxml')
    topfive = newsoup.find_all('td', class_='text-left visitedlyr', limit = 5)
    keys = ['1', '2', '3', '4', '5']
    values = []
    for song in topfive:
        values.append('%s by %s' % (song.a.b.text, song.a.b.next_element.next_element.next_element.text))
    # values = 
    print(values)
    # print(topfiveartists)



find()


# # Runs search()
# search()
# while search.again == 'y':
#     search()

# while not search.valid:
#     answers = ['1', '2']
#     answer = input("Sorry we couldn't find %s. Would you like to try another song [1]\nor quit [2]? " % (search.query))
#     while answer not in answers:
#         answer = input("Please use either 1 or 2 to answer. Would you like to try another song [1] or quit [2]? ")

#     if answer == '1':
#         search()

#     elif answer == '2':
#         break

# sys.exit()



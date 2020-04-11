"""Main file for Lyrics-Finder project, allows you to select azlyrics.com or genius.com as source"""
import sys

lyric_source = input('Would you like to use azlyrics.com [1] or genius.com? [2] ')
while lyric_source not in ['1', '2']:
    lyric_source = input('Please use either 1 or 2 to denote your answer. ')


def start():
    """Main function of file, executes searches based on preference"""
    if lyric_source == '1':
        from lyricsources import azlyricscom
        search = input('What song would you like to find the lyrics for today? ')
        result = directory(search)
        if result == None:
            azlyricscom.find(search)

        else:
            print('\n' + result)
            again()

    elif lyric_source == '2':
        from lyricsources import geniuscom
        search = input('What song would you like to find the lyrics for today? ')
        result = directory(search)
        if result == None:
            geniuscom.find(search)

        else:
            print('\n' + result)
            again()

def again():
    """Asks whether user has another song"""
    again = input('\nWould you like to try another song[1] or quit[2]? ')

    while again not in ['1', '2']:
        again = input("'%s' is an invalid answer. Please try again. " % (again))

    if again == '1': start()
    elif again == '2': sys.exit()

def directory(songname):
    """Lyrics-Finder has the ability to write lyrics to files, this function checks the directory for
    file before executing a web search to save time and resources
    """

    songname = songname.strip()
    songname = songname.split()
    songname = " ".join(songname)
    filename = f'{songname}.txt'

    try:
        file = open(filename, 'r')

    except:
        return None

    else:
        lyrics = file.readlines()
        lyrics = "".join(lyrics)
        file.close()
        return lyrics

if __name__ == '__main__':
    start() 
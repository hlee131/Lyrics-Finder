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

start()
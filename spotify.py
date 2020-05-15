import win32gui

def get_info_windows():
	"""
	Reads the window titles to get the data.
	Older Spotify versions simply use FindWindow for "SpotifyMainWindow",
	the newer ones create an EnumHandler and flood the list with
	Chrome_WidgetWin_0s

	Original Author: SwagLyrics on Github
	https://github.com/SwagLyrics/SwagLyrics-For-Spotify
	"""
	windows = []
	old_window = win32gui.FindWindow("SpotifyMainWindow", None)
	old = win32gui.GetWindowText(old_window)

	def find_spotify_uwp(hwnd, windows):
		text = win32gui.GetWindowText(hwnd)
		classname = win32gui.GetClassName(hwnd)
		if classname == "Chrome_WidgetWin_0" and len(text) > 0:
			windows.append(text)

	if old:
		windows.append(old)

	else:
		win32gui.EnumWindows(find_spotify_uwp, windows)

	# Local songs may only have a title field
	try:
		artist, track = windows[0].split(" - ", 1)

	except ValueError:
		artist = ''
		track = windows[0]

	except IndexError:
		return 'Spotify not running'

	# The window title is the default one when paused
	if windows[0].startswith('Spotify'):
		return 'Spotify paused'

	return f'{track} by {artist}'

if __name__ == "__main__":
	print(get_info_windows())

"""
Methods:
	- Play Music
	- Play SFX
"""

from pygame import mixer
from tkinter import SUNKEN, RAISED, Label
from random import randint
from mutagen.mp3 import MP3

class Player():
	def __init__(self, set_manager, sound_manager):
		mixer.init(frequency=44100)

		self.set_manager = set_manager
		self.sound_manager = sound_manager
		
		self.theme = None
		self.song = ""
		self.paused = True
		self.length = 0



	def set_volume(self, volume=-1):
		if volume == -1:
			mixer.music.set_volume(self.set_manager.settings["volume"] / 100)
		else:
			mixer.music.set_volume(volume / 100)


	def change_theme(self, theme):
		print(f'\nTheme: {theme}')

		self.theme = theme
		self.play()
		

	def play(self, song=None):
		if song == None:
			song_id = randint(0, len(self.sound_manager.themes[self.theme]) - 1)
			song_path = self.sound_manager.themes[self.theme][song_id]
			
			mixer.music.load(song_path)
			mixer.music.play(loops=0)

			self.length = MP3(song_path).info.length
			self.paused = False
			self.song = song_path

			print(f'Next Song: {song_path}')

		else:
			mixer.music.load(song)
			mixer.music.play(loops=0)

	def stop(self):
		self.paused = True
		self.theme = None
		self.song = ""
		mixer.music.stop()

	def pause(self):
		if self.paused:
			mixer.music.unpause()

		else:
			mixer.music.pause()

		self.paused = not self.paused

	def skip(self):
		if not self.theme == None:
			self.play()


	def play_sfx(self, sfx_path):
		sfx = mixer.Sound(sfx_path)

		mixer.Sound.set_volume(sfx, 4 * (self.set_manager.settings["volume"] / 100))
		mixer.Sound.play(sfx)

		print(f'\nSFX: {sfx}')


	def get_pos(self):
		return mixer.music.get_pos() / 1000

"""
Methods:
	- Play Music
	- Play SFX
"""

from pygame import mixer

class Player():
	def __init__(self, set_manager):
		mixer.init(frequency=44100)

		self.set_manager = set_manager


	def set_volume(self, volume=-1):
		if volume == -1:
			mixer.music.set_volume(self.set_manager.volume / 100)
		else:
			mixer.music.set_volume(volume / 100)

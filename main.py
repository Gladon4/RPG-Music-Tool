#!/bin/python

"""
Start the App
Methods:
	- Load Settings
	- Create Player
	- Create Tabs

Classes:
	- Tabs:
		- Main
		- Paths
		- Themes
		- Settings
		- SFX (potentially)
	- Player
"""

from player import Player
from settings_manager import Set_Manager


from tkinter import *


# --- Constants --- #
APP_NAME = "RPG Music Tool v06_dev"
START_SIZE = "800x800"

# --- Variables --- #


# --- Objects--- #
set_manager = Set_Manager()

player = Player(set_manager)

root = Tk()
# style = ttk.Style()


# Load settings and create the tab classes
def setup():
	set_manager.load_settings()

	player.set_volume()


	root.title(APP_NAME)
	root.geometry(START_SIZE)
	# style.layout('TNotebook.Tab', [])


# Run the app
def main():
	print("\n ---RPG MUSIC TOOL--- \n")

	root.mainloop()



if __name__ == "__main__":
	setup()
	main()


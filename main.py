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
from sound_manager import Sound_Manager
from main_tab import Main_Tab


from tkinter import *
from tkinter import ttk


# --- Constants --- #
APP_NAME = "RPG Music Tool v06_dev"
START_SIZE = "800x800"

# --- Variables --- #


# --- Objects--- #
set_manager = Set_Manager()
sound_manager = Sound_Manager(set_manager)
player = Player(set_manager, sound_manager)

root = Tk()

style = ttk.Style()
notebook = ttk.Notebook(root)

main_tab = Main_Tab(set_manager, sound_manager, notebook, player)


# Load settings and create the tab classes
def setup():
	set_manager.load_settings()
	set_manager.load_paths()

	sound_manager.load_themes()
	sound_manager.load_sfx()

	player.set_volume()


	root.title(APP_NAME)
	root.geometry(START_SIZE)

	# style.layout('TNotebook.Tab', [])
	notebook.pack(fill="both", expand=1)

	main_tab.create()
	notebook.add(main_tab.frame, text="Main")




# Run the app
def main():
	print("\n ---RPG MUSIC TOOL--- \n")

	root.mainloop()



if __name__ == "__main__":
	setup()
	main()


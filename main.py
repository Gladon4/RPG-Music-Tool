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
from managers.settings_manager import Set_Manager
from managers.sound_manager import Sound_Manager
from tabs.main_tab import Main_Tab
from tabs.settings_tab import Settings_Tab
from managers.tab_manager import Tab_Manager


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

# Tabs
tab_manager = Tab_Manager(notebook)

main_tab = Main_Tab(set_manager, sound_manager, tab_manager, notebook, player)
settings_tab = Settings_Tab(set_manager, tab_manager, notebook)


# Load settings and create the tab classes
def setup():
	set_manager.load_settings()
	set_manager.load_paths()

	sound_manager.load_themes()
	sound_manager.load_sfx()

	player.set_volume()


	root.title(APP_NAME)
	root.geometry(START_SIZE)

	style.layout('TNotebook.Tab', [])
	notebook.pack(fill="both", expand=1)

	main_tab.create()
	notebook.add(main_tab.frame, text="Main")

	settings_tab.create()
	notebook.add(settings_tab.frame, text="Settings")

	tab_manager.set_tabs({"main": main_tab.frame, 
						  "settings": settings_tab.frame})



# Run the app
def main():
	print("\n ---RPG MUSIC TOOL--- \n")

	root.mainloop()



if __name__ == "__main__":
	setup()
	main()


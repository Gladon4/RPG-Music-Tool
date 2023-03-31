"""
Methods:
	- Create GUI
	- File adder
	- Update
"""

from tkinter import *
import tkfilebrowser
import sys
import os

class Paths_Tab():
	def __init__(self, set_manager, tab_manager, notebook, sound_manager):
		self.set_manager = set_manager
		self.tab_manager = tab_manager
		self.notebook = notebook
		self.sound_manager = sound_manager
		self.paths = {}
		self.objects = {"labels" 	: [],
						"sec_labels": [],
						"buttons"	: []}

	def create(self, new=False):
		settings = self.set_manager.settings
		self.__load_imgs()

		# --- Main Frame --- #
		if (not new):
			self.frame = Frame(self.notebook, width=0, height=0, bg=settings["bg_color"])
			self.frame.grid_rowconfigure(0, weight=0)
			self.frame.grid_columnconfigure(0, weight=1)


		# --- Frames --- #

		self.navigation_buttons_frame = LabelFrame(self.frame, bg=settings["bg_color"], padx=0, borderwidth=0)
		self.navigation_buttons_frame.grid(row=0, column=1, rowspan=2, sticky="nw")

		self.list_frame = Frame(self.frame, bg=settings["sec_bg_color"], width=1000)
		self.list_frame.grid(row=1, column=0, pady=10)


		# --- Labels --- #

		self.label_title_paths = Label(self.frame, text="Music Directories", font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_paths.grid(row=0, column=0, pady=10)


		# --- Inputs --- #

		self.settings_button = Button(self.navigation_buttons_frame, command=lambda tab="settings": self.__select_tab(tab), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="top")

		self.add_button = Button(self.frame, text="Add Music Directory", command=self.__pinker_music, bg=settings["bg_color"], fg=settings["txt_color"], activebackground=settings["button_hov_color"])
		self.add_button.grid(row=2, column=0)


		# --- Paths list --- #

		for i, path in enumerate(self.set_manager.music_paths):
			path_delete_button = Button(self.list_frame, image=self.delete_image, command=lambda i=i: self.__delete(i), activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
			path_delete_button.grid(row=i, column=0, pady=2)
			path_label = Label(self.list_frame, text=path,font=("Helvetica",12), padx=5, bg=settings["sec_bg_color"], fg=settings["txt_color"])
			path_label.grid(row=i, column=1)
			self.paths[i] = [path_delete_button, path_label]


	def __pinker_music(self):
		dirs = tkfilebrowser.askopendirnames(title="Select your Music Directories", initialdir="/home/", okbuttontext="Select")
		i = len(self.set_manager.music_paths)

		for dir in dirs:
			path_delete_button = Button(self.list_frame, image=self.delete_image, command=lambda i=i: self.__delete(i), activebackground=self.set_manager.settings["button_hov_color"], bg=self.set_manager.settings["button_bg_color"])
			path_delete_button.grid(row=i, column=0)
			path_label = Label(self.list_frame, text=dir,font=("Helvetica",12), bg=self.set_manager.settings["sec_bg_color"], fg=self.set_manager.settings["txt_color"])
			path_label.grid(row=i, column=1)
			self.paths[i] = [path_delete_button, path_label]
			self.set_manager.music_paths += [dir+"/"]
			i += 1
		
		self.__update()
		self.set_manager.store_paths()
		self.sound_manager.load_themes()
		

	def __update(self):
		for path in self.paths:
			self.paths[path][0].grid(row=path, column=0)
			self.paths[path][1].grid(row=path, column=1)


	def __delete(self, index):
		self.paths[index][0].destroy()
		self.paths[index][1].destroy()
		del (self.paths[index])

		self.set_manager.music_paths = self.set_manager.music_paths[:index] + self.set_manager.music_paths[index+1:]

		new_paths = {}
		for i, p in enumerate(self.paths):
			new_paths[i] = self.paths[p]
			new_paths[i][0].config(command=lambda i=i: self.__delete(i))
		self.paths = new_paths

		self.set_manager.store_paths()
		self.sound_manager.load_themes()

	def __load_imgs(self):
		if getattr(sys, 'frozen', False):
			self.back_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/back_img.png"))
			self.delete_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/delete_img.png"))
			
		else:
			self.back_image = PhotoImage(file="img/back_img.png")
			self.delete_image = PhotoImage(file="img/delete_img.png")


	def __select_tab(self, tab):
		self.tab_manager.tabs["main"].update_elements()
		self.tab_manager.select(tab)

	def update_elements(self):
		pass
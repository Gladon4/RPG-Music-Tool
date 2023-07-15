"""
"""

from tkinter import *
from tkinter import ttk
import sys
import os

class Themes_Tab():
	def __init__(self, set_manager, sound_manager, tab_manager, notebook, player):
		self.set_manager = set_manager
		self.sound_manager = sound_manager
		self.tab_manager = tab_manager
		self.notebook = notebook
		self.player = player
		self.objects = {"labels" 	: [],
						"sec_labels": [],
						"buttons"	: []}



	def create(self, new=False):
		settings = self.set_manager.settings
		self.__load_imgs()
		self.__load_directories()
		self.current_path_index = 0	

		# --- Main Frame --- #
		if (not new):
			self.frame = Frame(self.notebook, width=0, height=0, bg=settings["bg_color"])
			self.frame.grid_rowconfigure(0, weight=0)
			self.frame.grid_columnconfigure(0, weight=1)
			

		# --- Frames --- #
		self.navigation_buttons_frame = LabelFrame(self.frame, bg=settings["bg_color"], padx=0, borderwidth=0)
		self.navigation_buttons_frame.place(relx=1.0, rely=0, anchor=NE)

		self.top_display_frame = Frame(self.frame, bg=settings["bg_color"], padx=5, pady=5, borderwidth=0)
		self.top_display_frame.grid(row=1, column=0)

		# --- Labels --- #
		self.label_title_themes = Label(self.frame, text="Music Themes", font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_themes.grid(row=0, column=0, pady=5)

		directory_label_string = self.__create_directory_label_string()
		self.label_current_directory = Label(self.top_display_frame, text=directory_label_string,font=("Helvetica",12), padx=5, pady=5, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_current_directory.grid(row=1, column=0, columnspan=2)

		# --- Inputs --- #
		self.settings_button = Button(self.navigation_buttons_frame, command=lambda tab="settings": self.__select_tab(tab), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="top")

		# -- Dropdown version
		""" 
		variable = StringVar(self.frame)
		variable.set("COLOURS")

		option_menu = OptionMenu(self.frame, variable, "Yellow",
                         "Blue", "Green", "Purple",
                         "Black", "White")
		option_menu.config(bg=settings["bg_color"], fg=settings["txt_color"], activebackground=settings["button_hov_color"])
		
		option_menu.grid(row=2, column=0)
		"""

		# -- sliding select
	
		self.previous_page_button = Button(self.top_display_frame, text="<", command=self.__previous_page, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], padx=10)
		self.previous_page_button.grid(row=0, column=0, sticky=E, padx=5, ipadx=30)
		if self.current_path_index == 0:
			self.previous_page_button.config(state=DISABLED)

		self.next_page_button = Button(self.top_display_frame, text=">", command=self.__next_page, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], padx=10)
		self.next_page_button.grid(row=0, column=1, sticky=W, padx=5, ipadx=30)
		if (self.current_path_index + 1) == len(self.paths):
			self.next_page_button.config(state=DISABLED)
		

	def __destroy(self):
		for category in self.objects:
			for object in self.objects[category]:
				if type(object) != str:
					object.destroy()
				else:
					self.objects[category][object].destroy()
				

	def update_elements(self):
		self.frame.config(bg=self.set_manager.settings["bg_color"])
		self.__destroy()
		self.create(True)


	def __select_tab(self, tab):
		self.tab_manager.select(tab)

	
	def __load_directories(self):
		self.paths = self.set_manager.music_paths

	def __create_directory_label_string(self):
		MIN_STRING_LENGTH = 40
		path_string = self.paths[self.current_path_index]
		if len(path_string) >= MIN_STRING_LENGTH:
			return "  " + path_string + "  "
	
		missing_space = MIN_STRING_LENGTH - len(path_string)
		padding = " " * (int(missing_space / 2) + 2)
		return padding + path_string + padding

	def __previous_page(self):
		self.current_path_index = self.current_path_index-1
		if self.current_path_index == 0:
			self.previous_page_button.config(state=DISABLED)
		if not (self.current_path_index + 1) == len(self.paths):
			self.next_page_button.config(state=ACTIVE)
		self.__set_directory()

	def __next_page(self):
		self.current_path_index = self.current_path_index+1
		if (self.current_path_index + 1) == len(self.paths):
			self.next_page_button.config(state=DISABLED)
		if not self.current_path_index == 0:
			self.previous_page_button.config(state=ACTIVE)
		self.__set_directory()

	def __set_directory(self):
		directory_label_string = self.__create_directory_label_string()
		self.label_current_directory.config(text=directory_label_string)


	# Images
	def __load_imgs(self):
		if getattr(sys, 'frozen', False):
			self.back_image		= PhotoImage(file=os.path.join(sys._MEIPASS, "img/back_img.png"))
			self.stop_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/stop_img.png"))
			self.play_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/play_img.png"))
			
		else:
			self.back_image 	= PhotoImage(file="img/back_img.png")
			self.stop_image 	= PhotoImage(file="img/stop_img.png")
			self.play_image 	= PhotoImage(file="img/play_img.png")

		self.play_image_small = self.play_image.subsample(3, 3)
		self.stop_image_small = self.stop_image.subsample(3, 3)
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

		# --- Main Frame --- #
		if (not new):
			self.frame = Frame(self.notebook, width=0, height=0, bg=settings["bg_color"])
			self.frame.grid_rowconfigure(0, weight=0)
			self.frame.grid_columnconfigure(0, weight=1)
			

		# --- Frames --- #
		self.navigation_buttons_frame = LabelFrame(self.frame, bg=settings["bg_color"], padx=0, borderwidth=0)
		self.navigation_buttons_frame.grid(row=0, column=1, rowspan=2, sticky="nw")


		# --- Labels --- #


		# --- Inputs --- #
		self.settings_button = Button(self.navigation_buttons_frame, command=lambda tab="settings": self.__select_tab(tab), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="top")


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
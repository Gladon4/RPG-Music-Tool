from appdirs import user_config_dir
from configparser import ConfigParser
import csv
from os.path import isdir, isfile
from os import mkdir
import sys


class Set_Manager():
	def __init__(self):
		self.path = user_config_dir("rpg-mt", "Gladon")
		if not isdir(self.path): 
			self.create_config_dir()
		self.config = ConfigParser()

		self.settings = {}
		self.music_paths = []
		self.sfx_paths = []


	# --- Settings --- #

	def load_settings(self):
		if isfile(self.path + "/config.ini"):
			config_file = self.path + "/config.ini"
			self.config.read(config_file)

			color_settings = self.config["color_settings"]
			app_settings = self.config["app_settings"]

			self.settings = {# Colors
				 "bg_color"			: color_settings["bg_color"],
				 "sec_bg_color"		: color_settings["sec_bg_color"],
				 "button_bg_color"	: color_settings["button_color"],
				 "button_hov_color"	: color_settings["button_color_hover"],
				 "txt_color"		: color_settings["text_color"],
				 # App Settings
				 "volume"			: int(float(app_settings["volume"])),
				 "ui_scale"			: int(app_settings["ui_scale"]),
				 "row_length"		: int(app_settings["row_length"]),
				 "sfx_on_themes"	: int(app_settings["sfx_on_themes"])
				 }

		else:
			self.__write_default_settings()
			self.load_settings()

	def store_settings(self):
		self.config["color_settings"] = {"bg_color" 			: self.settings["bg_color"],
										 "sec_bg_color" 		: self.settings["sec_bg_color"],
										 "button_color" 		: self.settings["button_bg_color"],
										 "button_color_hover" 	: self.settings["button_hov_color"],
										 "text_color" 			: self.settings["txt_color"]}

		self.config["app_settings"] = {"ui_scale" 		: self.settings["ui_scale"],
									   "row_length"		: self.settings["row_length"],
									   "volume" 		: self.settings["volume"],
									   "sfx_on_themes" 	: self.settings["sfx_on_themes"]}

		with open(self.path + '/config.ini', 'w') as configfile:
			self.config.write(configfile)  

	def create_config_dir(self):
		if sys.platform.startswith('linux'):
			try:
				mkdir(self.path)
			except:
				pass
			
		elif sys.platform.startswith('win32'):
			try:
				path2 = "\\".join(self.path.split("\\")[:-1])
				mkdir(path2)
				mkdir(self.path)
			except:
				pass

	def __write_default_settings(self):
		# --- Defaults --- #
		# Color
		bg_col =      	"#91a3c4"
		sec_bg_col =    "#9baecb"
		but_col =       "#7b8cb3"
		sec_but_col =   "#668bb0"
		text_col =      "#323232"

		# App Settings
		ui_scale =      2
		row_length =    6
		def_vol =       15
		def_sfx_pos =   1

		self.config["color_settings"] = {"bg_color" 			: bg_col,
										 "sec_bg_color" 		: sec_bg_col,
										 "button_color" 		: but_col,
										 "button_color_hover" 	: sec_but_col,
										 "text_color" 			: text_col}

		self.config["app_settings"] = {"ui_scale" 		: ui_scale,
									   "row_length"		: row_length,
									   "volume" 		: def_vol,
									   "sfx_on_themes" 	: def_sfx_pos}

		with open(self.path + '/config.ini', 'w') as configfile:
			self.config.write(configfile)


	# --- Paths --- #

	def load_paths(self):
		self.music_paths = []
		self.sfx_paths = []
		
		# --- Music --- #
		if not isfile(self.path + "/paths.csv"):
			open(self.path + "/paths.csv", 'a').close()
		with open(self.path + "/paths.csv", "r", encoding="utf-8-sig") as csv_file:
			list = csv.reader(csv_file, delimiter=',', quotechar='|')
			for row in list:
				if row != []:
					self.music_paths = row

		# --- SFX --- #
		if not isfile(self.path + "/sfx-paths.csv"):
			open(self.path + "/sfx-paths.csv", 'a').close()
		with open(self.path + "/sfx-paths.csv", "r", encoding="utf-8-sig") as csv_file:
			list = csv.reader(csv_file, delimiter=',', quotechar='|')
			for row in list:
				if row != []:
					self.sfx_paths = row

	def store_paths(self):
		pass
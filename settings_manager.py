from appdirs import user_config_dir
from configparser import ConfigParser



class Set_Manager():
	def __init__(self):
		self.volume = 0
		self.path = user_config_dir("rpg-mt", "Gladon")
		self.config = ConfigParser()


	def load_settings(self):

		try:
			with open(self.path + "/config.ini") as file:
				pass

			# --- Config --- #
			config_file = self.path + "/config.ini"
			self.config.read(config_file)

			# Color
			color_settings = self.config["color_settings"]

			BACKGROUND_COLOR = color_settings["bg_color"]
			BUTTON_BG = color_settings["button_color"]
			BUTTON_HOVER = color_settings["button_color_hover"]
			TEXT_COLOR = color_settings["text_color"]
			SEC_BG_COLOR = color_settings["sec_bg_color"]

			# App Settings
			app_settings = self.config["app_settings"]
			UI_SCALE = int(app_settings["ui_scale"])
			ROW_LENGTH = int(app_settings["row_length"])
			volume = int(float(app_settings["volume"]))
			SFX_ON_THEMES = int(app_settings["sfx_on_themes"])

		except:
			self.write_default_settings()
			self.load_settings()


	def write_default_settings(self):
		# --- Defaults --- #
		# Color
		bg_col =      "#91a3c4"
		sec_bg_col =    "#9baecb"
		but_col =       "#7b8cb3"
		sec_but_col =   "#668bb0"
		text_col =      "#323232"

		# App Settings
		ui_scale =      2
		row_length =    6
		def_vol =       15
		def_sfx_pos =   1

		self.config["color_settings"] = {"bg_color" : bg_col,
		                            "sec_bg_color" : sec_bg_col,
		                            "button_color" : but_col,
		                            "button_color_hover" : sec_but_col,
		                            "text_color" : text_col}

		self.config["app_settings"] = {"ui_scale" : ui_scale,
		                            "row_length": row_length,
		                            "volume" : def_vol,
		                            "sfx_on_themes" : def_sfx_pos}

		with open(self.path + '/config.ini', 'w') as configfile:
		    self.config.write(configfile)  
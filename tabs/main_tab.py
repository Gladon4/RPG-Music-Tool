"""
Methods:
	- Create GUI
	- Call Player
	- Switch Tab
	- Update Player
		- Progressbar
		- Volume (Settings)
	- Update Element Settings
"""

from tkinter import Frame, Button, LabelFrame, Label, PhotoImage, ttk
import sys, time, os

class Main_Tab():
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

		self.theme_buttons_frame = LabelFrame(self.frame, text="", bg=settings["bg_color"], padx=25, borderwidth=0, pady=10)
		self.theme_buttons_frame.grid(row=1, column=0)

		self.navigation_buttons_frame = LabelFrame(self.frame, bg=settings["bg_color"], padx=0, borderwidth=0)
		self.navigation_buttons_frame.place(relx=1.0, rely=0, anchor="ne")

		self.lower_frame = LabelFrame(self.frame, text="", pady=5, padx=15, bg=settings["bg_color"], borderwidth=0)
		self.lower_frame.grid(row=4, column=0)

		self.status = LabelFrame(self.lower_frame, text="", pady=15, padx=15, bg=settings["sec_bg_color"], borderwidth=1)
		self.status.grid(row=0, column=0, padx=2)

		self.volume_frame = LabelFrame(self.lower_frame, text="", pady=15, padx=15, bg=settings["sec_bg_color"],)
		self.volume_frame.grid(row=0, column=1, padx=2)

		self.volume_plus_minus_frame = LabelFrame(self.lower_frame, text="", pady=2, padx=2, bg=settings["bg_color"], borderwidth=0)
		self.volume_plus_minus_frame.grid(row=0, column=2, padx=2)


		self.objects["labels"] 		+= [self.theme_buttons_frame, self.lower_frame, self.volume_plus_minus_frame, self.navigation_buttons_frame]
		self.objects["sec_labels"] 	+= [self.status, self.volume_frame]


		# --- Labels --- #

		self.label_current_song = Label(self.frame, text="No Song Playing",font = ("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_current_song.grid(row=2, column=0)

		self.label_current_song_path = Label(self.frame, text="No Song Playing",font = ("Helvetica",12), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_current_song_path.grid(row=3, column=0)

		self.label_current_theme = Label(self.frame, text="No Theme Selected", font = ("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_current_theme.grid(row=0, column=0, pady=5)

		self.label_duration_song = Label(self.status, text="00:00 / 00:00", font=("Helvetica",12), bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_duration_song.grid(row=0, column=4, padx=5)

		self.song_progress = ttk.Progressbar(self.status, orient="horizontal", length=280, mode='determinate')
		self.song_progress.grid(row=0, column=3, padx=5)

		self.label_volume = Label(self.volume_frame, text=str(settings["volume"]),font=("Helvetica",10,'bold'), bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_volume.grid(row=1, column=0)


		self.objects["labels"] 	+= [self.label_current_song, self.label_current_song_path, self.label_current_theme, 
									self.label_duration_song, self.label_volume]


		# --- Inputs --- #

		self.button_stop = Button(self.status, command=self.__stop, image=self.stop_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.button_stop.grid(row=0, column=0)

		self.button_pause = Button(self.status, command=self.__pause, image=self.pause_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.button_pause.grid(row=0, column=1)

		self.button_skip = Button(self.status, command=self.__skip, image=self.skip_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.button_skip.grid(row=0, column=2)

		self.volume_changer = ttk.Scale(self.volume_frame, from_=100, to=0, orient="vertical", value=int(settings["volume"]), command=self.__change_volume, length=120)
		self.volume_changer.grid(row=0, column=0)

		self.volume_up_button = Button(self.volume_plus_minus_frame, command=self.__volume_up, image=self.plus_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.volume_up_button.grid(row=0, column=1, pady=5)

		self.volume_down_button = Button(self.volume_plus_minus_frame, command=self.__volume_down, image=self.minus_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.volume_down_button.grid(row=1, column=1, pady=5)

		self.settings_button = Button(self.navigation_buttons_frame, command=lambda x=self: self.tab_manager.select("settings"), image=self.settings_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="bottom")


		self.objects["buttons"]	+= [self.button_stop, self.button_pause, self.button_skip, self.volume_down_button,
									self.volume_up_button, self.settings_button]


		self.__create_theme_buttons()

		
		if settings["sfx_on_themes"]: 
			self.sfx_buttons_frame = LabelFrame(self.frame, text="", bg=settings["bg_color"], padx=25, borderwidth=0, pady=5)
			self.sfx_buttons_frame.grid(row=6, column=0)

			self.label_sfx = Label(self.frame, text="Sound Effects", font = ("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
			self.label_sfx.grid(row=5, column=0, pady=5)


			self.objects["labels"]	+= [self.sfx_buttons_frame, self.label_sfx]

			self.__create_sfx_buttons()

		self.__song_duration()


	def __destroy(self):
		for category in self.objects:
			for object in self.objects[category]:
				object.destroy()

	
	def update_elements(self):
		self.frame.config(bg=self.set_manager.settings["bg_color"])
		self.__destroy()
		self.create(True)

	# Media Methods
	def __play(self, theme):
		self.theme_buttons[theme].config(bg=self.set_manager.settings["button_hov_color"], relief="sunken")

		if not self.player.theme == None and not theme == self.player.theme:
			self.theme_buttons[self.player.theme].config(bg=self.set_manager.settings["button_bg_color"], relief="raised")

		self.player.change_theme(theme)
		self.__update_music_labels()

	def __pause(self):
		if self.player.paused:
			self.button_pause.config(image=self.pause_image)
		else:
			self.button_pause.config(image=self.play_image)

		self.player.pause()

	def __stop(self):
		if self.player.theme == None:
			return
		
		self.theme_buttons[self.player.theme].config(bg=self.set_manager.settings["button_bg_color"], relief="raised")
		self.player.stop()
		self.__update_music_labels()

	def __skip(self):
		self.player.skip()
		self.__update_music_labels()


	# Loop Method to update to song progress
	def __song_duration(self):
		if not self.player.paused:
			length = self.player.length

			current_time = self.player.get_pos()
			converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
			
			converted_length = time.strftime('%M:%S', time.gmtime(length))
			song_time = str(converted_current_time) + " / " + str(converted_length)

			self.label_duration_song.config(text=song_time)
			self.song_progress['value'] = current_time / length * 100

			if current_time <= 0 and not self.player.paused:
				song = self.player.play()
				self.__update_music_labels()

		self.label_duration_song.after(500, self.__song_duration)

	def __update_music_labels(self):
		if self.player.theme == None:
			self.label_current_theme.config(text="No Theme Selected")
			self.label_current_song.config(text="No Song Playing")
			self.label_current_song_path.config(text="No Song Playing")

			self.label_duration_song.config(text="00:00/00:00")
			self.song_progress['value'] = 0

		else:
			if sys.platform.startswith('linux'):
				song = self.player.song.split("/")[-1].split(".mp3")[0]
				path = self.player.song.split("/")[-2]
				
			elif sys.platform.startswith('win32'):
				song = self.player.song.split("\\")[-1].split(".mp3")[0]
				path = self.player.song.split("\\")[-2]

			if self.set_manager.settings["full_paths_main"]:
				path = self.player.song

			self.label_current_theme.config(text=self.player.theme)
			self.label_current_song.config(text=song)
			self.label_current_song_path.config(text=path)


	# Volume Change Methods
	def __set_volume(self, volume, button=False):
		self.set_manager.settings["volume"] = volume
		self.set_manager.store_settings()

		self.label_volume.config(text=str(int(volume)))
		if button: self.volume_changer.set(volume)
		self.player.set_volume()

	def __change_volume(self, pos):
		self.__set_volume(int(float(pos)))

	def __volume_up(self):
		volume = self.set_manager.settings["volume"] + 1
		self.__set_volume(volume, True)

	def __volume_down(self):
		volume = self.set_manager.settings["volume"] - 1
		self.__set_volume(volume, True)



	# Create Button Methods
	def __create_theme_buttons(self):
		settings = self.set_manager.settings
		self.theme_buttons = {}

		i = 0
		for _theme in self.sound_manager.themes:
			text = _theme
			theme_play_button = Button(self.theme_buttons_frame,
										text=text, compound="center", borderwidth=0,
										activebackground=settings["button_hov_color"],
										bg=settings["button_bg_color"],
										fg=settings["txt_color"],
										height=int(2.5*settings["ui_scale"]), 
										width=int(5*settings["ui_scale"]),
										command=lambda _theme=_theme: self.__play(_theme))


			theme_play_button.grid(row = (i // settings["row_length"] + 1), column = (i % settings["row_length"]))
			
			if self.player.theme == _theme:
				theme_play_button.config(bg=settings["button_hov_color"], relief="sunken")
			
			i += 1

			self.theme_buttons[_theme] = theme_play_button


	def __create_sfx_buttons(self):
		settings = self.set_manager.settings
		temp_sfx_list = []

		for path in self.set_manager.sfx_paths:
			for sfx in self.sound_manager.sfxs[path]:
				temp_sfx_list += [path + sfx]

		self.sfx_buttons = []

		i = 0
		for sfx in temp_sfx_list:
			text = ""
			if sys.platform.startswith('win32'):
				text = sfx.split("\\")
				text = text[-1].split(".mp3")[0]

			elif sys.platform.startswith('linux'):
				text = sfx.split("/")
				text = text[-1].split(".mp3")[0]

			# self.sfx_play_button = Button(sfx_buttons_frame, text=text, command=lambda sfx=sfx: play_sfx(sfx), compound=CENTER, borderwidth=0, activebackground=BUTTON_HOVER, bg=BUTTON_BG, fg=TEXT_COLOR, height=int(2.5*UI_SCALE), width=int(5*UI_SCALE))
			self.sfx_play_button = Button(self.sfx_buttons_frame,
										text=text, compound="center", borderwidth=0,
										activebackground=settings["button_hov_color"],
										bg=settings["button_bg_color"],
										fg=settings["txt_color"],
										height=int(2.5*settings["ui_scale"]), 
										width=int(5*settings["ui_scale"]),
										command=lambda sfx=sfx: self.player.play_sfx(sfx))


			self.sfx_play_button.grid(row=(i // settings["row_length"] + 1), column=(i % settings["row_length"]))
			
			self.sfx_buttons.append(self.sfx_play_button)

			i += 1


	# Images
	def __load_imgs(self):
		if getattr(sys, 'frozen', False):
			self.stop_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/stop_img.png"))
			self.skip_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/skip_img.png"))
			self.pause_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/pause_img.png"))
			self.play_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/play_img.png"))
			self.plus_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/plus_img.png"))
			self.minus_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/minus_img.png"))
			self.settings_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/settings_img.png"))
			
		else:
			self.stop_image 	= PhotoImage(file="img/stop_img.png")
			self.skip_image 	= PhotoImage(file="img/skip_img.png")
			self.pause_image 	= PhotoImage(file="img/pause_img.png")
			self.play_image 	= PhotoImage(file="img/play_img.png")
			self.plus_image 	= PhotoImage(file="img/plus_img.png")
			self.minus_image 	= PhotoImage(file="img/minus_img.png")
			self.settings_image = PhotoImage(file="img/settings_img.png")
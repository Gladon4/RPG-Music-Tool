from tkinter import *
import sys, os

class Themes_Tab():
	def __init__(self, set_manager, sound_manager, tab_manager, notebook, player):
		self.set_manager = set_manager
		self.sound_manager = sound_manager
		self.tab_manager = tab_manager
		self.notebook = notebook
		self.player = player
		self.page_number = 0
		self.songs_per_page = 12
		self.current_song_playing = None
		self.objects = {"labels" 	: [],
						"sec_labels": [],
						"buttons"	: [],
						"frames" 	: []}



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
		self.navigation_buttons_frame.place(relx=1.0, rely=0, anchor="ne")

		self.top_display_frame = Frame(self.frame, bg=settings["bg_color"], padx=5, pady=5, borderwidth=0)
		self.top_display_frame.grid(row=1, column=0)

		self.list_frame = Frame(self.frame, bg=settings["sec_bg_color"], width=1000)
		self.list_frame.grid(row=2, column=0, pady=10, padx=10, sticky="n")
		self.objects["frames"].append(self.list_frame)

		self.page_navigation_frame = Frame(self.frame, bg=settings["bg_color"], width=1000)
		self.page_navigation_frame.grid(row=3, column=0)
		# self.page_navigation_frame.grid_columnconfigure(1, minsize=350)

		# self.frame.grid_rowconfigure(1, minsize=550)

		# --- Labels --- #
		self.label_title_themes = Label(self.frame, text="Music Themes", font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_themes.grid(row=0, column=0, pady=5)

		directory_label_string = self.__create_directory_label_string()
		self.label_current_directory = Label(self.top_display_frame, text=directory_label_string,font=("Helvetica",12), padx=5, pady=5, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_current_directory.grid(row=1, column=0, columnspan=2)
		self.objects["labels"].append(self.label_current_directory)

		# --- Inputs --- #
		self.settings_button = Button(self.navigation_buttons_frame, command=lambda tab="settings": self.__select_tab(tab), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="top")
	
		self.previous_path_button = Button(self.top_display_frame, text="<", command=self.__previous_path, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], padx=10)
		self.previous_path_button.grid(row=0, column=0, sticky="e", padx=5, ipadx=30)
		if self.current_path_index == 0:
			self.previous_path_button.config(state="disabled")

		self.next_path_button = Button(self.top_display_frame, text=">", command=self.__next_path, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], padx=10)
		self.next_path_button.grid(row=0, column=1, sticky="w", padx=5, ipadx=30)
		if (self.current_path_index + 1) == len(self.paths):
			self.next_path_button.config(state="disabled")


		self.previous_page_button = Button(self.page_navigation_frame, text="<", command=self.__previous_page, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], padx=10)
		self.previous_page_button.grid(row=0, column=0, sticky="e", padx=5, ipadx=30)
		if self.page_number == 0:
			self.previous_page_button.config(state="disabled")

		self.next_page_button = Button(self.page_navigation_frame, text=">", command=self.__next_page, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.next_page_button.grid(row=0, column=1, sticky="w", padx=5, ipadx=30)
		if (self.page_number + 1) * self.songs_per_page >= len(list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())):
			self.next_page_button.config(state="disabled")

		self.__create_list()




	def __create_list(self):
		settings = self.set_manager.settings
		songs = list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())
		per_page = self.songs_per_page
		page = self.page_number
		self.play_buttons = [None for _ in range(per_page)]
		self.theme_boxes = [None for _ in range(per_page)]
		self.songs_labels = [None for _ in range(per_page)]

		SONGS_IN_PATH = len(songs)
		REMAING_PATHS = SONGS_IN_PATH - per_page * page
		for i in range(min(per_page, REMAING_PATHS)):
			index_with_offset = per_page * page + i
			song = songs[index_with_offset]
						
			song_play_button = Button(self.list_frame, image=self.play_image_small, command=lambda i=index_with_offset: self.__play(i), activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
			song_play_button.grid(row=i, column=0, pady=2, padx=10)

			song_label = Label(self.list_frame, text=song, font=("Helvetica",12), padx=5, bg=settings["sec_bg_color"], fg=settings["txt_color"])
			song_label.grid(row=i, column=1)

			song_themes = Text(self.list_frame, width=45, height=3)
			song_themes.grid(row=i, column=2, padx=10)

			self.play_buttons[i] = song_play_button
			self.theme_boxes[i] = song_themes
			self.songs_labels[i] = song_label


	def __destroy_list(self):
		for i in range(self.songs_per_page):
			if self.play_buttons[i] == None:
				continue
		
			self.play_buttons[i].destroy()
			self.theme_boxes[i].destroy()
			self.songs_labels[i].destroy()


	def __play(self, i):
		index_in_list = i % self.songs_per_page
		if index_in_list == self.current_song_playing:
			self.__stop()
			return

		if self.current_song_playing != None:
			self.play_buttons[self.current_song_playing].config(image=self.play_image_small)

		self.current_song_playing = index_in_list
		self.play_buttons[index_in_list].config(image=self.stop_image_small)

		song_path = self.paths[self.current_path_index] + list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())[i]

		self.player.stop()
		self.player.play(song_path)

	def __stop(self):
		if self.current_song_playing != None:
			self.play_buttons[self.current_song_playing].config(image=self.play_image_small)
		
		self.current_song_playing = None
		self.player.stop()

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
		self.__stop()
		self.tab_manager.select(tab)

	
	def __load_directories(self):
		self.paths = self.set_manager.music_paths


	def __create_directory_label_string(self):
		MIN_STRING_LENGTH = 40

		if self.set_manager.settings["full_paths_settings"]:
			path_string = self.paths[self.current_path_index]
	
		elif sys.platform.startswith('linux'):
			path_string = self.paths[self.current_path_index].split("/")[-2]
				
		elif sys.platform.startswith('win32'):
			path_string = self.paths[self.current_path_index].split("\\")[-2]
				
		
		if len(path_string) >= MIN_STRING_LENGTH:
			return "  " + path_string + "  "
	
		missing_space = MIN_STRING_LENGTH - len(path_string)
		padding = " " * (int(missing_space / 2) + 2)
		return padding + path_string + padding


	def __previous_page(self):
		self.page_number -= 1
		if self.page_number == 0:
			self.previous_page_button.config(state="disabled")
		if not (self.page_number + 1)* self.songs_per_page >= len(list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())):
			self.next_page_button.config(state="active")
		
		self.__stop()
		self.__destroy_list()
		self.__create_list()


	def __next_page(self):
		self.page_number += 1
		if (self.page_number + 1)* self.songs_per_page >= len(list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())):
			self.next_page_button.config(state="disabled")
		if not self.page_number == 0:
			self.previous_page_button.config(state="active")
		
		self.__stop()
		self.__destroy_list()
		self.__create_list()


	def __previous_path(self):
		self.current_path_index -= 1

		if self.current_path_index == 0:
			self.previous_path_button.config(state="disabled")
		if not (self.current_path_index + 1) == len(self.paths):
			self.next_path_button.config(state="active")
		
		self.__set_directory()

	def __next_path(self):
		self.current_path_index += 1
		if (self.current_path_index + 1) == len(self.paths):
			self.next_path_button.config(state="disabled")
		if not self.current_path_index == 0:
			self.previous_path_button.config(state="active")
		self.__set_directory()

	def __set_directory(self):
		directory_label_string = self.__create_directory_label_string()
		self.label_current_directory.config(text=directory_label_string)

		self.page_number = 0
		self.previous_page_button.config(state="disabled")
		self.next_page_button.config(state="disable")
		if not (self.page_number + 1)* self.songs_per_page >= len(list(self.sound_manager.songs[self.paths[self.current_path_index]].keys())):
			self.next_page_button.config(state="active")
		
		self.__stop()
		self.__destroy_list()
		self.__create_list()


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

		self.play_image_small = self.play_image.subsample(2, 2)
		self.stop_image_small = self.stop_image.subsample(2, 2)
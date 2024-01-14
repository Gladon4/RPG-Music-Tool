"""
Methods:
	- Create GUI
	- File adder
	- Update
"""

from tkinter import Frame, Label, LabelFrame, Button, PhotoImage
import tkfilebrowser
import sys, os
if sys.platform.startswith('win32'):
	# Required on windows for tkfilebrowser
	import win32com

class Paths_Tab():
	def __init__(self, set_manager, tab_manager, notebook, sound_manager):
		self.set_manager = set_manager
		self.tab_manager = tab_manager
		self.notebook = notebook
		self.sound_manager = sound_manager
		self.page_number = 0
		self.paths_per_page = 12
		self.paths = {}
		self.objects = {"labels" 	: [],
						"sec_labels": [],
						"buttons"	: [],
						"list_elems": [],
						"frames": []}

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
		self.navigation_buttons_frame.place(relx=1.0, rely=0, anchor="ne")

		self.list_frame = Frame(self.frame, bg=settings["sec_bg_color"], width=1000)
		self.list_frame.grid(row=1, column=0, pady=10, sticky="n")
		self.objects["frames"].append(self.list_frame)

		self.page_navigation_frame = Frame(self.frame, bg=settings["bg_color"], width=1000)
		self.page_navigation_frame.grid(row=2, column=0)
		self.page_navigation_frame.grid_columnconfigure(1, minsize=350)

		self.frame.grid_rowconfigure(1, minsize=550)


		# --- Labels --- #

		self.label_title_paths = Label(self.frame, text="Music Directories", font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_paths.grid(row=0, column=0, pady=5)


		# --- Inputs --- #

		self.settings_button = Button(self.navigation_buttons_frame, command=lambda tab="settings": self.__select_tab(tab), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="top")

		self.add_button = Button(self.page_navigation_frame, text="Add Music Directory", command=self.__music_path_picker, bg=settings["bg_color"], fg=settings["txt_color"], activebackground=settings["button_hov_color"])
		self.add_button.grid(row=0, column=1)
		
		self.previous_page_button = Button(self.page_navigation_frame, text="<", command=self.__previous_page, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.previous_page_button.grid(row=0, column=0)
		if self.page_number == 0:
			self.previous_page_button.config(state="disabled")

		self.next_page_button = Button(self.page_navigation_frame, text=">", command=self.__next_page, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.next_page_button.grid(row=0, column=2)
		if (self.page_number + 1) * self.paths_per_page >= len(self.set_manager.music_paths):
			self.next_page_button.config(state="disabled")

		self.__create_list()


	def __create_list(self):
		settings = self.set_manager.settings
		per_page = self.paths_per_page
		page = self.page_number

		REMAING_PATHS = len(self.set_manager.music_paths) - per_page * page
		for i in range(min(per_page, REMAING_PATHS)):
			index_with_offset = per_page * page + i
			path = self.set_manager.music_paths[index_with_offset]

			path_delete_button = Button(self.list_frame, image=self.delete_image, command=lambda i=index_with_offset: self.__delete(i), activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
			path_delete_button.grid(row=i, column=0, pady=2)


			if settings["full_paths_settings"]:
				path_text = path
				
			elif sys.platform.startswith('linux'):
				path_text = path.split("/")[-2]
				
			elif sys.platform.startswith('win32'):
				path_text = path.split("\\")[-2]
			
			path_label = Label(self.list_frame, text=path_text,font=("Helvetica",12), padx=5, bg=settings["sec_bg_color"], fg=settings["txt_color"])
			path_label.grid(row=i, column=1)
			self.paths[i] = [path_delete_button, path_label]


	def __next_page(self):
		for path in self.paths:
			self.paths[path][0].destroy()
			self.paths[path][1].destroy()
	
		self.page_number += 1
		self.paths = {}
		self.__create_list()
		
		if (self.page_number + 1)* self.paths_per_page >= len(self.set_manager.music_paths):
			self.next_page_button.config(state="disabled")
		if not self.page_number == 0:
			self.previous_page_button.config(state="active")

	
	def __previous_page(self):
		for path in self.paths:
			self.paths[path][0].destroy()
			self.paths[path][1].destroy()
	
		self.page_number -= 1
		self.paths = {}
		self.__create_list()

		if self.page_number == 0:
			self.previous_page_button.config(state="disabled")
		if not (self.page_number + 1)* self.paths_per_page >= len(self.set_manager.music_paths):
			self.next_page_button.config(state="active")


	def __music_path_picker(self):
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


	def __destroy(self):
		for category in self.objects:
			for object in self.objects[category]:
				object.destroy()

		for path in self.paths:
			self.paths[path][0].destroy()
			self.paths[path][1].destroy()


	def update_elements(self):
		self.frame.config(bg=self.set_manager.settings["bg_color"])
		self.__destroy()
		self.create(True)
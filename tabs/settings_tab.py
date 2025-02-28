from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
import sys, os

class Settings_Tab():
	def __init__(self, set_manager, tab_manager, notebook):
		self.set_manager = set_manager
		self.tab_manager = tab_manager
		self.notebook = notebook
		self.objects = {"labels" 	: 	[],
						"sec_labels": 	[],
						"buttons"	: 	[],
						"color_elems" :	{}}

		self.change = False

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

		self.ui_setting_frame = LabelFrame(self.frame, font=("Helvetica",15), pady=15, padx=15, bg=settings["sec_bg_color"], borderwidth=0)
		self.ui_setting_frame.grid(row=1, column=0)
		

		# --- Labels --- #

		self.label_title_app_settings = Label(self.frame, text="Application Settings",font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_app_settings.grid(row=0, column=0, pady=5)

		self.label_subtitle_ui_scale = Label(self.ui_setting_frame, text="Theme Button Scale",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"], height=2)
		self.label_subtitle_ui_scale.grid(row=0, column=0, sticky="nw")

		self.ui_scale_label = Label(self.ui_setting_frame, text=settings["ui_scale"], font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"], width=1)
		self.ui_scale_label.grid(row=0, column=2, sticky="n")

		self.label_subtitle_row_lenght = Label(self.ui_setting_frame, text="Themes Buttons per Row",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"], height=2)
		self.label_subtitle_row_lenght.grid(row=2, column=0, sticky="nw")

		self.row_length_label = Label(self.ui_setting_frame, text=settings["row_length"], font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"], width=1)
		self.row_length_label.grid(row=2, column=2, sticky="n")

		self.sfx_on_themes_label = Label(self.ui_setting_frame, text="Display SFX on Main Page",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"], height=2)
		self.sfx_on_themes_label.grid(row=3, column=0, sticky="nw")

		self.full_path_on_main_label = Label(self.ui_setting_frame, text="Display Full Paths on Main Page",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"], height=2)
		self.full_path_on_main_label.grid(row=4, column=0, sticky="nw")

		self.full_path_in_settings_label = Label(self.ui_setting_frame, text="Display Full Paths in Settings",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"], height=2)
		self.full_path_in_settings_label.grid(row=5, column=0, sticky="nw")

		# self.sfx_on_themes_label = Label(self.ui_setting_frame, text="Display SFX on Themes Tab", font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		# self.sfx_on_themes_label.grid(row=3, column=0, pady=10)


		# --- Inputs --- #

		self.settings_button = Button(self.navigation_buttons_frame, command=lambda tab="main": self.__select_tab(tab), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="top")

		self.paths_button = Button(self.navigation_buttons_frame, command=lambda tab="song_paths": self.__select_tab(tab), image=self.list_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.paths_button.pack(side="top")

		self.paths_button = Button(self.navigation_buttons_frame, command=lambda tab="sfx_paths": self.__select_tab(tab), image=self.list_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.paths_button.pack(side="top")

		self.themes_button = Button(self.navigation_buttons_frame, command=lambda tab="themes": self.__select_tab(tab), image=self.themes_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.themes_button.pack(side="top")



		self.ui_scale_slider = ttk.Scale(self.ui_setting_frame, from_=1, to=5, value=settings["ui_scale"], command=self.__change_ui_scale, length=150)
		self.ui_scale_slider.grid(row=0, column=1, sticky="n")

		self.row_length_slider = ttk.Scale(self.ui_setting_frame,from_=3, to=10, value=settings["row_length"], command=self.__change_row_length, length=150)
		self.row_length_slider.grid(row=2, column=1, sticky="n")

		self.sfx_on_themes_check = Label(self.ui_setting_frame, image=self.check_off, cursor="hand2", bg=settings["sec_bg_color"], fg="#ffffff")
		self.sfx_on_themes_check.bind("<Button-1>", self.__change_sfx_on_themes)
		self.sfx_on_themes_check.grid(row=3, column=1, sticky="ne")
		if settings["sfx_on_themes"]: self.sfx_on_themes_check.config(image=self.check_on)

		self.full_path_on_main_check = Label(self.ui_setting_frame, image=self.check_off, cursor="hand2", bg=settings["sec_bg_color"], )
		self.full_path_on_main_check.bind("<Button-1>", self.__full_path_on_main)
		self.full_path_on_main_check.grid(row=4, column=1, sticky="ne")
		if settings["full_paths_main"]: self.full_path_on_main_check.config(image=self.check_on)


		self.full_path_in_settings_check = Label(self.ui_setting_frame, image=self.check_off, cursor="hand2", bg=settings["sec_bg_color"], )
		self.full_path_in_settings_check.bind("<Button-1>", self.__full_path_in_settings)
		self.full_path_in_settings_check.grid(row=5, column=1, sticky="ne")
		if settings["full_paths_settings"]: self.full_path_in_settings_check.config(image=self.check_on)
		


		# -- Color Settings -- #
		self.label_title_color_settings = Label(self.frame, text="Color Settings",font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_color_settings.grid(row=3, column=0, pady=10)

		colors_frame = LabelFrame(self.frame, bg=settings["bg_color"], borderwidth=0)
		colors_frame.grid(row=4, column=0)


		colors = {x: self.set_manager.settings[x] for x in ["bg_color", "sec_bg_color", "button_bg_color", "button_hov_color", "txt_color"]}
		colorNames = {"bg_color": "Background Colour", "sec_bg_color": "Secondary Backgroud Colour", "button_bg_color": "Button Colour", "button_hov_color": "Hover Button Colour", "txt_color": "Text Colour"}

		for i, color in enumerate(colors):
			label_frame = LabelFrame(colors_frame, bg=settings["sec_bg_color"], borderwidth=0)
			label_frame.grid(row=i//3+1, column=i % 3, padx=6, pady=6)
			color_name_label = Label(label_frame, text=colorNames[color], fg=settings["txt_color"], bg=settings["sec_bg_color"])
			color_name_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=3, pady=(3,0))
			color_label_frame = LabelFrame(label_frame, bg=settings["bg_color"], borderwidth=3)
			color_label_frame.grid(row=1, column=0, padx=3, pady=3)
			color_label = Label(color_label_frame, width=18, height=9, bg=colors[color])
			color_label.pack()
			picker_button = Button(label_frame, text="Pick\nColour", command=lambda color=color, name=colorNames[color]: self.__change_color(color, name), activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], fg=settings["txt_color"], height=3, width=5)
			picker_button.grid(row=1, column=1, padx=5)

			self.objects["color_elems"][color] = color_label



		# -- Reset Settings -- #
		reset_button = Button(self.frame, text="Reset Settings", command=self.__reset_settings, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], height=3, width=12)
		reset_button.grid(row=5, column=0)



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
		if (self.change):
			self.tab_manager.update_all_tab_elements()
			self.change = False
		self.tab_manager.select(tab)


	def __load_imgs(self):
		if getattr(sys, 'frozen', False):
			self.back_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/back_img.png"))
			self.list_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/list_img.png"))
			self.themes_image = PhotoImage(file=os.path.join(sys._MEIPASS, "img/label.png"))
			
		else:
			self.back_image = PhotoImage(file="img/back_img.png")
			self.list_image = PhotoImage(file="img/list_img.png")
			self.themes_image = PhotoImage(file="img/label.png")
			self.check_on = PhotoImage(file="img/check_on.png").subsample(4,4)
			self.check_off = PhotoImage(file="img/check_off.png").subsample(4,4)
		
	def __change_ui_scale(self, pos):
		self.change = True

		new_scale = int(float(pos))
		
		self.set_manager.settings["ui_scale"] = new_scale
		self.set_manager.store_settings()

		self.ui_scale_label.config(text=new_scale)
		self.ui_scale_slider.config(value=new_scale)

	def __change_row_length(self, pos):
		self.change = True

		new_length = int(float(pos))
		
		self.set_manager.settings["row_length"] = new_length
		self.set_manager.store_settings()

		self.row_length_label.config(text=new_length)
		self.row_length_slider.config(value=new_length)
	
	def __change_sfx_on_themes(self, e):
		self.change = True
		self.set_manager.settings["sfx_on_themes"] = 0 if self.set_manager.settings["sfx_on_themes"] else 1
		if self.set_manager.settings["sfx_on_themes"]: 
			self.sfx_on_themes_check.config(image=self.check_on)
		else: 
			self.sfx_on_themes_check.config(image=self.check_off)
		self.set_manager.store_settings()

	def __full_path_on_main(self, e):
		self.change = True
		self.set_manager.settings["full_paths_main"] = 0 if self.set_manager.settings["full_paths_main"] else 1
		if self.set_manager.settings["full_paths_main"]: 
			self.full_path_on_main_check.config(image=self.check_on)
		else: 
			self.full_path_on_main_check.config(image=self.check_off)
		self.set_manager.store_settings()
	
	def __full_path_in_settings(self, e):
		self.change = True
		self.set_manager.settings["full_paths_settings"] = 0 if self.set_manager.settings["full_paths_settings"] else 1
		if self.set_manager.settings["full_paths_settings"]: 
			self.full_path_in_settings_check.config(image=self.check_on)
		else: 
			self.full_path_in_settings_check.config(image=self.check_off)
		self.set_manager.store_settings()

	def __reset_settings(self):
		self.set_manager.reset_to_defaults()
		self.tab_manager.update_all_tab_elements()

	def __change_color(self, color, name):
		self.change = True

		chosenColor = askcolor(self.set_manager.settings[color], title="Choose " + name)[1]

		if chosenColor:
			self.objects["color_elems"][color].config(bg=chosenColor)

		self.set_manager.settings[color] = chosenColor
		self.set_manager.store_settings()

		self.update_elements()

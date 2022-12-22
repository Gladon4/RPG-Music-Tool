"""
Methods:
	- Create GUI
	- Save Settings
"""

from tkinter import *
from tkinter import ttk
import sys

class Settings_Tab():
	def __init__(self, set_manager, tab_manager, notebook):
		self.set_manager = set_manager
		self.tab_manager = tab_manager
		self.notebook = notebook
		self.objects = {"labels" 	: [],
						"sec_labels": [],
						"buttons"	: []}


	def create(self):
		settings = self.set_manager.settings
		self.__load_imgs()

		# --- Main Frame --- #
		self.frame = Frame(self.notebook, width=0, height=0, bg=settings["bg_color"])
		self.frame.grid_rowconfigure(0, weight=0)
		self.frame.grid_columnconfigure(0, weight=1)


		# --- Frames --- #

		self.navigation_buttons_frame = LabelFrame(self.frame, bg=settings["bg_color"], padx=0, borderwidth=0)
		self.navigation_buttons_frame.grid(row=0, column=1, rowspan=2, sticky="nw")

		self.ui_setting_frame = LabelFrame(self.frame, text="UI Settings", font=("Helvetica",15), pady=15, padx=15, bg=settings["sec_bg_color"], borderwidth=0)
		self.ui_setting_frame.grid(row=2, column=0)
		

		# --- Labels --- #

		self.label_title_app_settings = Label(self.frame, text="Application Settings",font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		self.label_title_app_settings.grid(row=0, column=0)

		self.label_subtitle_ui_scale = Label(self.ui_setting_frame, text="Theme Button Scale",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_subtitle_ui_scale.grid(row=0, column=0)

		self.label_subtitle_ui_scale = Label(self.ui_setting_frame, text="Theme Button Scale",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_subtitle_ui_scale.grid(row=0, column=0)

		self.ui_scale_label = Label(self.ui_setting_frame, text=settings["ui_scale"], font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.ui_scale_label.grid(row=0, column=2)

		self.label_subtitle_row_lenght = Label(self.ui_setting_frame, text="Themes Buttons per Row",font=("Helvetica",12), padx=15, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.label_subtitle_row_lenght.grid(row=2, column=0)

		self.row_length_label = Label(self.ui_setting_frame, text=settings["row_length"], font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.row_length_label.grid(row=2, column=2)

		self.sfx_on_themes_label = Label(self.ui_setting_frame, text="Display SFX on Themes Tab", font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"])
		self.sfx_on_themes_label.grid(row=3, column=0, pady=10)


		# --- Inputs --- #

		self.settings_button = Button(self.navigation_buttons_frame, command=lambda x=self: self.tab_manager.select("main"), image=self.back_image, borderwidth=0, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"])
		self.settings_button.pack(side="bottom")

		self.ui_scale_slider = ttk.Scale(self.ui_setting_frame, from_=1, to=5, value=settings["ui_scale"], length=200)
		self.ui_scale_slider.grid(row=0, column=1, pady=10)

		self.row_length_slider = ttk.Scale(self.ui_setting_frame, from_=3, to=10, value=settings["row_length"], length=200)
		self.row_length_slider.grid(row=2, column=1, pady=10)

		self.sfx_on_themes_checkbox = Checkbutton(self.ui_setting_frame, text="  (Requires Restart)  ", height=2, bg=settings["button_bg_color"], activebackground=settings["button_hov_color"])
		self.sfx_on_themes_checkbox.grid(row=3, column=1)
		if settings["sfx_on_themes"]: self.sfx_on_themes_checkbox.select()
		
		# -- Color Settings -- #

		"""
		bg_color = settings["bg_color"]
		but_col = settings["button_bg_color"]
		but_hov_col = settings["button_hov_color"]
		settings["txt_color"] = settings["txt_color"]
		sec_bg_col = settings["sec_bg_color"]
		
		colors = {"Background Color":bg_color, "Secondary Background Color": sec_bg_col, "Text Color":settings["txt_color"], "Primary Button Color":but_col, "Secondary Button Color":but_hov_col}
		color_elems = [] 
		
		label_title_color_settings = Label(self.frame, text="Color Settings",font=("Helvetica",20), bg=settings["bg_color"], fg=settings["txt_color"])
		label_title_color_settings.pack(pady=15)

		colors_frame = LabelFrame(self.frame, bg=settings["bg_color"], borderwidth=0)
		colors_frame.pack()

		i = 0
		for color in colors:
			label_frame = LabelFrame(colors_frame, bg=settings["sec_bg_color"], text=color)
			label_frame.grid(row=i//3+1, column=i % 3, padx=6, pady=6)
			color_label_frame = LabelFrame(label_frame, bg=settings["bg_color"], borderwidth=3)
			color_label_frame.grid(row=0, column=0)
			color_label = Label(color_label_frame, width=18, height=9, bg=colors[color])
			color_label.pack()
			picker_button = Button(label_frame, text="Pick Color", command=lambda i=i: change_color(i), activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], height=4, width=6)
			picker_button.grid(row=0, column=1, padx=5)

			color_elems += [[label_frame, color_label_frame, color_label, picker_button, color]]

			i += 1

	

		# -- Reset Settings -- #
		reset_button = Button(self.frame, text="Reset Settings", command=reset_settings, activebackground=settings["button_hov_color"], bg=settings["button_bg_color"], height=3, width=12)
		reset_button.pack(pady=15)
		"""


	def update_elements(self):
		pass


	def __load_imgs(self):
		if getattr(sys, 'frozen', False):
			self.back_image 	= PhotoImage(file=os.path.join(sys._MEIPASS, "img/back_img.png"))
			
		else:
			self.back_image 	= PhotoImage(file="img/back_img.png")
		
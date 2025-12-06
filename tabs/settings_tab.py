import os
import sys
from tkinter import Button, Frame, Label, LabelFrame, PhotoImage
from tkinter.colorchooser import askcolor
from tkinter.ttk import Scale, Style
from turtle import width


class SettingSlider:
    def __init__(self, title: Label, scale: Scale, label: Label) -> None:
        self.title: Label = title
        self.scale: Scale = scale
        self.label: Label = label


class SettingsTab:
    def __init__(self, set_manager, tab_manager, notebook):
        self.set_manager = set_manager
        self.tab_manager = tab_manager
        self.notebook = notebook
        self.objects = {
            "labels": [],
            "sec_labels": [],
            "buttons": [],
            "color_elems": {},
        }

        self.change = False

    def create(self, new=False):
        settings = self.set_manager.settings
        self.__load_imgs()

        # --- Main Frame --- #
        if not new:
            self.frame = Frame(
                self.notebook, width=0, height=0, bg=settings["bg_color"]
            )
            self.frame.grid_rowconfigure(0, weight=0)
            self.frame.grid_columnconfigure(0, weight=1)

        # --- Frames --- #

        self.navigation_buttons_frame = LabelFrame(
            self.frame, bg=settings["bg_color"], padx=0, borderwidth=0
        )
        self.navigation_buttons_frame.place(relx=1.0, rely=0, anchor="ne")

        self.ui_setting_frame = LabelFrame(
            self.frame,
            font=("Helvetica", 15),
            pady=15,
            padx=15,
            bg=settings["sec_bg_color"],
            borderwidth=0,
        )
        self.ui_setting_frame.grid(row=1, column=0)

        self.label_title_app_settings = Label(
            self.frame,
            text="Application Settings",
            font=("Helvetica", 20),
            bg=settings["bg_color"],
            fg=settings["txt_color"],
        )
        self.label_title_app_settings.grid(row=0, column=0, pady=5)

        style = Style()

        style.configure(
            "Custom.Horizontal.TScale",
            troughcolor=settings["sec_bg_color"],
            background=settings["button_hov_color"],
            lightcolor="black",
            darkcolor="black",
            sliderlength=30 * (settings["ui_scale"] / 100),
            sliderthickness=20 * (settings["ui_scale"] / 100),
        )

        self.ui_scale = self.__make_setting_slider(
            self.ui_setting_frame,
            row=0,
            title="UI Scale",
            current_value=settings["ui_scale"],
            min_value=100,
            max_value=300,
            command=self.__change_ui_scale,
            settings=settings,
        )

        self.theme_button_scale = self.__make_setting_slider(
            self.ui_setting_frame,
            row=1,
            title="Theme Button Scale",
            current_value=settings["theme_button_scale"],
            min_value=1,
            max_value=6,
            command=self.__change_theme_button_scale,
            settings=settings,
        )

        self.row_length = self.__make_setting_slider(
            self.ui_setting_frame,
            row=2,
            title="Theme Buttons per Row",
            current_value=settings["row_length"],
            min_value=3,
            max_value=10,
            command=self.__change_row_length,
            settings=settings,
        )

        # --- Labels --- #

        self.sfx_on_themes_label = Label(
            self.ui_setting_frame,
            text="Display SFX on Main Page",
            font=("Helvetica", 12),
            padx=15,
            bg=settings["sec_bg_color"],
            fg=settings["txt_color"],
            height=2,
        )
        self.sfx_on_themes_label.grid(row=3, column=0, sticky="nw")

        self.full_path_on_main_label = Label(
            self.ui_setting_frame,
            text="Display Full Paths on Main Page",
            font=("Helvetica", 12),
            padx=15,
            bg=settings["sec_bg_color"],
            fg=settings["txt_color"],
            height=2,
        )
        self.full_path_on_main_label.grid(row=4, column=0, sticky="nw")

        self.full_path_in_settings_label = Label(
            self.ui_setting_frame,
            text="Display Full Paths in Settings",
            font=("Helvetica", 12),
            padx=15,
            bg=settings["sec_bg_color"],
            fg=settings["txt_color"],
            height=2,
        )
        self.full_path_in_settings_label.grid(row=5, column=0, sticky="nw")

        # self.sfx_on_themes_label = Label(self.ui_setting_frame, text="Display SFX on Themes Tab", font=("Helvetica",12), padx=10, bg=settings["sec_bg_color"], fg=settings["txt_color"])
        # self.sfx_on_themes_label.grid(row=3, column=0, pady=10)

        # --- Inputs --- #

        self.settings_button = Button(
            self.navigation_buttons_frame,
            command=lambda tab="main": self.__select_tab(tab),
            image=self.back_image,
            borderwidth=0,
            activebackground=settings["button_hov_color"],
            bg=settings["button_bg_color"],
        )
        self.settings_button.pack(side="top")

        self.paths_button = Button(
            self.navigation_buttons_frame,
            command=lambda tab="song_paths": self.__select_tab(tab),
            image=self.list_image,
            borderwidth=0,
            activebackground=settings["button_hov_color"],
            bg=settings["button_bg_color"],
        )
        self.paths_button.pack(side="top")

        self.paths_button = Button(
            self.navigation_buttons_frame,
            command=lambda tab="sfx_paths": self.__select_tab(tab),
            image=self.list_image,
            borderwidth=0,
            activebackground=settings["button_hov_color"],
            bg=settings["button_bg_color"],
        )
        self.paths_button.pack(side="top")

        self.themes_button = Button(
            self.navigation_buttons_frame,
            command=lambda tab="themes": self.__select_tab(tab),
            image=self.themes_image,
            borderwidth=0,
            activebackground=settings["button_hov_color"],
            bg=settings["button_bg_color"],
        )
        self.themes_button.pack(side="top")

        self.sfx_on_themes_check = Label(
            self.ui_setting_frame,
            image=self.check_off,
            cursor="hand2",
            bg=settings["sec_bg_color"],
            fg="#ffffff",
        )
        self.sfx_on_themes_check.bind("<Button-1>", self.__change_sfx_on_themes)
        self.sfx_on_themes_check.grid(row=3, column=1, sticky="ns")
        if settings["sfx_on_themes"]:
            self.sfx_on_themes_check.config(image=self.check_on)

        self.full_path_on_main_check = Label(
            self.ui_setting_frame,
            image=self.check_off,
            cursor="hand2",
            bg=settings["sec_bg_color"],
        )
        self.full_path_on_main_check.bind("<Button-1>", self.__full_path_on_main)
        self.full_path_on_main_check.grid(row=4, column=1, sticky="ns")
        if settings["full_paths_main"]:
            self.full_path_on_main_check.config(image=self.check_on)

        self.full_path_in_settings_check = Label(
            self.ui_setting_frame,
            image=self.check_off,
            cursor="hand2",
            bg=settings["sec_bg_color"],
        )
        self.full_path_in_settings_check.bind(
            "<Button-1>", self.__full_path_in_settings
        )
        self.full_path_in_settings_check.grid(row=5, column=1, sticky="ns")
        if settings["full_paths_settings"]:
            self.full_path_in_settings_check.config(image=self.check_on)

        # -- Color Settings -- #
        self.label_title_color_settings = Label(
            self.frame,
            text="Color Settings",
            font=("Helvetica", 20),
            bg=settings["bg_color"],
            fg=settings["txt_color"],
        )
        self.label_title_color_settings.grid(row=3, column=0, pady=10)

        colors_frame = LabelFrame(self.frame, bg=settings["bg_color"], borderwidth=0)
        colors_frame.grid(row=4, column=0)

        colors = {
            x: self.set_manager.settings[x]
            for x in [
                "bg_color",
                "sec_bg_color",
                "button_bg_color",
                "button_hov_color",
                "txt_color",
            ]
        }
        colorNames = {
            "bg_color": "Primary Background Colour",
            "sec_bg_color": "Secondary Backgroud Colour",
            "button_bg_color": "Primary Accent Colour",
            "button_hov_color": "Secondary Accent Colour",
            "txt_color": "Text Colour",
        }

        for i, color in enumerate(colors):
            label_frame = LabelFrame(
                colors_frame, bg=settings["sec_bg_color"], borderwidth=0
            )
            label_frame.grid(row=i // 3 + 1, column=i % 3, padx=6, pady=6)
            color_name_label = Label(
                label_frame,
                text=colorNames[color],
                fg=settings["txt_color"],
                bg=settings["sec_bg_color"],
            )
            color_name_label.grid(
                row=0, column=0, columnspan=2, sticky="w", padx=3, pady=(3, 0)
            )
            color_label_frame = LabelFrame(
                label_frame, bg=settings["bg_color"], borderwidth=3
            )
            color_label_frame.grid(row=1, column=0, padx=3, pady=3)
            color_label = Button(
                color_label_frame,
                image=self.eyedropper_image,
                width=2 * settings["ui_scale"],
                height=2 * settings["ui_scale"],
                bg=colors[color],
                activebackground=settings["button_hov_color"],
                fg=settings["txt_color"],
                command=lambda color=color, name=colorNames[color]: self.__change_color(
                    color, name
                ),
            )
            color_label.pack()

            self.objects["color_elems"][color] = color_label

        # -- Reset Settings -- #
        reset_button = Button(
            self.frame,
            text="Reset Settings",
            command=self.__reset_settings,
            activebackground=settings["button_hov_color"],
            bg=settings["button_bg_color"],
            height=3,
            width=12,
        )
        reset_button.grid(row=5, column=0)

    def __make_setting_slider(
        self, frame, row, title, current_value, min_value, max_value, command, settings
    ) -> SettingSlider:
        title_label = Label(
            frame,
            text=title,
            font=("Helvetica", 12),
            padx=15,
            bg=settings["sec_bg_color"],
            fg=settings["txt_color"],
            height=2,
        )
        title_label.grid(row=row, column=0, sticky="nw")

        scale = Scale(
            frame,
            from_=min_value,
            to=max_value,
            value=current_value,
            command=command,
            length=2 * settings["ui_scale"],
            style="Custom.Horizontal.TScale",
        )
        scale.grid(row=row, column=1, sticky="n")

        label = Label(
            frame,
            text=current_value,
            font=("Helvetica", 12),
            padx=10,
            bg=settings["sec_bg_color"],
            fg=settings["txt_color"],
            width=1,
        )
        label.grid(row=row, column=2, sticky="n")

        return SettingSlider(title_label, scale, label)

    def __destroy(self):
        for category in self.objects:
            for object in self.objects[category]:
                if type(object) is not str:
                    object.destroy()
                else:
                    self.objects[category][object].destroy()

    def update_elements(self):
        self.frame.config(bg=self.set_manager.settings["bg_color"])
        self.__destroy()
        self.create(True)

    def __select_tab(self, tab):
        if self.change:
            self.tab_manager.update_all_tab_elements()
            self.change = False
        self.tab_manager.select(tab)

    def __load_imgs(self):
        if getattr(sys, "frozen", False):
            self.back_image = PhotoImage(
                file=os.path.join(sys._MEIPASS, "img/back_img.png")
            )
            self.list_image = PhotoImage(
                file=os.path.join(sys._MEIPASS, "img/list_img.png")
            )
            self.themes_image = PhotoImage(
                file=os.path.join(sys._MEIPASS, "img/label.png")
            )
            self.eyedropper_image = PhotoImage(
                file=os.path.join(sys._MEIPASS, "img/eyedropper.png")
            )
            self.check_on = PhotoImage(
                file=os.path.join(sys._MEIPASS, "img/check_on.png")
            ).subsample(4)
            self.check_off = PhotoImage(
                file=os.path.join(sys._MEIPASS, "img/check_off.png")
            ).subsample(4)
            self.empty_image = PhotoImage(width=1, height=1)

        else:
            self.back_image = PhotoImage(file="img/back_img.png")
            self.list_image = PhotoImage(file="img/list_img.png")
            self.themes_image = PhotoImage(file="img/label.png")
            self.eyedropper_image = PhotoImage(file="img/eyedropper.png")
            self.check_on = PhotoImage(file="img/check_on.png").subsample(4)
            self.check_off = PhotoImage(file="img/check_off.png").subsample(4)
            self.empty_image = PhotoImage(width=1, height=1)

    def __change_ui_scale(self, pos):
        self.change = True

        new_scale = int((int(float(pos)) // 10) * 10)

        self.set_manager.settings["ui_scale"] = new_scale
        self.set_manager.store_settings()

        self.ui_scale.label.config(text=new_scale)
        self.ui_scale.scale.config(value=new_scale)

    def __change_theme_button_scale(self, pos):
        self.change = True

        new_scale = int(float(pos))

        self.set_manager.settings["theme_button_scale"] = new_scale
        self.set_manager.store_settings()

        self.theme_button_scale.label.config(text=new_scale)
        self.theme_button_scale.scale.config(value=new_scale)

    def __change_row_length(self, pos):
        self.change = True

        new_length = int(float(pos))

        self.set_manager.settings["row_length"] = new_length
        self.set_manager.store_settings()

        self.row_length.label.config(text=new_length)
        self.row_length.scale.config(value=new_length)

    def __change_sfx_on_themes(self, _):
        self.change = True
        self.set_manager.settings["sfx_on_themes"] = (
            0 if self.set_manager.settings["sfx_on_themes"] else 1
        )
        if self.set_manager.settings["sfx_on_themes"]:
            self.sfx_on_themes_check.config(image=self.check_on)
        else:
            self.sfx_on_themes_check.config(image=self.check_off)
        self.set_manager.store_settings()

    def __full_path_on_main(self, _):
        self.change = True
        self.set_manager.settings["full_paths_main"] = (
            0 if self.set_manager.settings["full_paths_main"] else 1
        )
        if self.set_manager.settings["full_paths_main"]:
            self.full_path_on_main_check.config(image=self.check_on)
        else:
            self.full_path_on_main_check.config(image=self.check_off)
        self.set_manager.store_settings()

    def __full_path_in_settings(self, _):
        self.change = True
        self.set_manager.settings["full_paths_settings"] = (
            0 if self.set_manager.settings["full_paths_settings"] else 1
        )
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

        chosenColor = askcolor(
            self.set_manager.settings[color], title="Choose " + name
        )[1]

        if chosenColor is None:
            return

        self.objects["color_elems"][color].config(bg=chosenColor)

        self.set_manager.settings[color] = chosenColor
        self.set_manager.store_settings()

        self.update_elements()

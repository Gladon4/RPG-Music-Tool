from tkinter import Button, Event, EventType, Label, ttk
from tkinter.colorchooser import askcolor
from tkinter.ttk import Scale, Style

from include.tab import Tab
from managers.image_manager import ImageManager
from managers.settings_manager import SetttingsManager
from managers.tab_manager import TabManager


class SettingSlider:
    def __init__(self, title: Label, scale: Scale, label: Label) -> None:
        self.title: Label = title
        self.scale: Scale = scale
        self.label: Label = label


class SettingsTab(Tab):
    def __init__(
        self,
        settings_manager: SetttingsManager,
        tab_manager: TabManager,
        image_manager: ImageManager,
        notebook: ttk.Notebook,
    ) -> None:
        super().__init__(settings_manager, tab_manager, image_manager, notebook)

        self.settings_manager: SetttingsManager = settings_manager
        self.tab_manager: TabManager = tab_manager
        self.notebook = notebook

        self.change = False

        self.create(True)

    def add_navigation_button(self, destination: str, image: str) -> Button:
        navigation_button = super().add_navigation_button(destination, image)

        navigation_button.config(command=lambda: self.__select_tab(destination))

        return navigation_button

    def __select_tab(self, tab):
        if self.change:
            self.tab_manager.update_all_tab_elements()
        self.tab_manager.select(tab)

    def create(self, new: bool = False):
        super().create(new)

        settings = self.settings_manager.settings

        # --- Frames --- #
        self.ui_setting_frame = self.add_frame(self.frame, bg="sec_bg_color")
        self.ui_setting_frame.grid(row=1, column=0)

        self.app_settings_label = self.add_label(
            self.frame,
            text="Application Settings",
            font_size=2,
        )
        self.app_settings_label.grid(row=0, column=0, pady=5)

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

        self.font_size = self.__make_setting_slider(
            self.ui_setting_frame,
            row=3,
            title="Font Size",
            current_value=settings["font_size"],
            min_value=8,
            max_value=30,
            command=self.__change_font_size,
            settings=settings,
        )

        self.sfx_tab_text = {0: "Off", 1: "On Themes Tab", 2: "Separate Tab"}
        self.sfx_tab = self.__make_setting_slider(
            self.ui_setting_frame,
            row=4,
            title="SFX Location",
            current_value=settings["sfx_tab"],
            min_value=0,
            max_value=2,
            command=self.__change_sfx_tab,
            settings=settings,
        )
        self.sfx_tab.scale.grid(row=4, column=1, columnspan=1, sticky="w")
        self.sfx_tab.label.grid(row=4, column=2, columnspan=2, sticky="w")
        self.sfx_tab.scale.config(length=settings["ui_scale"])
        self.sfx_tab.label.config(text=self.sfx_tab_text[settings["sfx_tab"]])

        # --- Labels --- #
        self.full_path_on_main_label = self.add_label(
            self.ui_setting_frame,
            text="Display Full Paths on Themes Tab",
            bg="sec_bg_color",
        )
        self.full_path_on_main_label.grid(row=5, column=0, sticky="w", pady=7)

        self.full_path_in_settings_label = self.add_label(
            self.ui_setting_frame,
            text="Display Full Paths in Settings",
            bg="sec_bg_color",
        )
        self.full_path_in_settings_label.grid(row=6, column=0, sticky="w", pady=7)

        # --- Inputs --- #

        self.add_navigation_button(destination="themes", image="tag")
        self.add_navigation_button(destination="sfx_paths", image="folder_managed")
        self.add_navigation_button(destination="song_paths", image="folder_managed")
        self.add_navigation_button(destination="main", image="back")

        self.full_path_on_main_check = self.add_label(
            self.ui_setting_frame, bg="sec_bg_color"
        )
        self.full_path_on_main_check.config(
            image=self.image_manager.images["check_off"],
            cursor="hand2",
        )
        self.full_path_on_main_check.bind("<Button-1>", self.__full_path_on_main)
        self.full_path_on_main_check.grid(row=5, column=1, sticky="wns")
        if settings["full_paths_main"]:
            self.full_path_on_main_check.config(
                image=self.image_manager.images["check_on"]
            )

        self.full_path_in_settings_check = self.add_label(
            self.ui_setting_frame, bg="sec_bg_color"
        )
        self.full_path_in_settings_check.config(
            image=self.image_manager.images["check_off"],
            cursor="hand2",
        )
        self.full_path_in_settings_check.bind(
            "<Button-1>", self.__full_path_in_settings
        )
        self.full_path_in_settings_check.grid(row=6, column=1, sticky="wns")
        if settings["full_paths_settings"]:
            self.full_path_in_settings_check.config(
                image=self.image_manager.images["check_on"]
            )

        # -- Color Settings -- #
        self.label_title_color_settings = self.add_label(
            self.frame,
            text="Color Settings",
            font_size=2,
        )
        self.label_title_color_settings.grid(row=3, column=0, pady=10)

        self.colors_frame = self.add_frame(self.frame)
        self.colors_frame.grid(row=4, column=0)

        colors = {
            x: self.settings_manager.settings[x]
            for x in [
                "bg_color",
                "sec_bg_color",
                "button_bg_color",
                "button_hov_color",
                "txt_color",
            ]
        }
        colorNames = {
            "bg_color": "Primary Background",
            "sec_bg_color": "Secondary Backgroud",
            "button_bg_color": "Primary Accent",
            "button_hov_color": "Secondary Accent",
            "txt_color": "Text",
        }

        self.color_labels = []
        for i, color in enumerate(colors):
            frame = self.add_frame(self.colors_frame, bg="sec_bg_color")
            frame.grid(row=i // 3 + 1, column=i % 3, padx=6, pady=6)
            color_name_label = self.add_label(
                frame,
                text=colorNames[color],
                bg="sec_bg_color",
                wraplength=2.5 * settings["ui_scale"],
            )
            color_name_label.config(justify="left")
            color_name_label.grid(
                row=0, column=0, columnspan=2, sticky="w", padx=3, pady=(3, 0)
            )
            image = "eyedropper"
            if color == "txt_color":
                image = "eyedropper_inverse"
            color_label = self.add_button(
                frame,
                image=image,
                scale=1.75,
                command=lambda i=i, name=colorNames[color]: self.__change_color(
                    i, name
                ),
            )
            color_label.config(
                bg=colors[color],
                activebackground=colors[color],
                highlightthickness=7,
                highlightbackground=colors[color],
            )
            color_label.bind(
                "<Enter>",
                func=lambda e, j=i, col=colors[color]: self.__color_hover(e, j, col),
            )
            color_label.bind(
                "<Leave>",
                func=lambda e, j=i, col=colors[color]: self.__color_hover(e, j, col),
            )
            color_label.grid(row=1, column=0)

            self.color_labels.append(color_label)

        # -- Reset Settings -- #
        self.reset_button = self.add_button(
            self.frame,
            text="Reset Settings",
            command=self.__reset_settings,
            scale=0.6,
            wraplength=60,
        )
        self.reset_button.config()
        self.reset_button.grid(row=5, column=0)

        self.navigation_buttons_frame.tkraise()

    def __color_hover(self, e: Event, index: int, color: str):
        color_picker: Button = self.color_labels[index]

        if e.type == EventType.Enter:
            if color == self.settings_manager.settings["button_hov_color"]:
                color = self.settings_manager.settings["bg_color"]
            else:
                color = self.settings_manager.settings["button_hov_color"]
            color_picker.config(highlightbackground=color)
        elif e.type == EventType.Leave:
            color_picker.config(highlightbackground=color)

    def __make_setting_slider(
        self, frame, row, title, current_value, min_value, max_value, command, settings
    ) -> SettingSlider:
        title_label = self.add_label(frame, text=title, bg="sec_bg_color")
        title_label.grid(row=row, column=0, sticky="w")

        scale = Scale(
            frame,
            from_=min_value,
            to=max_value,
            value=current_value,
            command=command,
            length=2 * settings["ui_scale"],
            style="Custom.Horizontal.TScale",
        )
        scale.grid(row=row, column=1, sticky="ns", pady=7, columnspan=2)
        self.widgets.append(scale)

        label = self.add_label(frame, text=current_value, bg="sec_bg_color")
        label.grid(row=row, column=3, sticky="ns", padx=3)

        return SettingSlider(title_label, scale, label)

    def __change_sfx_tab(self, pos):
        self.change = True

        new_value = int(float(pos))

        self.settings_manager.settings["sfx_tab"] = new_value
        self.settings_manager.store_settings()

        self.sfx_tab.label.config(text=self.sfx_tab_text[new_value])
        self.sfx_tab.scale.config(value=new_value)

    def __change_ui_scale(self, pos):
        self.change = True

        new_scale = int((int(float(pos)) // 10) * 10)

        self.settings_manager.settings["ui_scale"] = new_scale
        self.settings_manager.store_settings()

        self.ui_scale.label.config(text=new_scale)
        self.ui_scale.scale.config(value=new_scale)

    def __change_theme_button_scale(self, pos):
        self.change = True

        new_scale = int(float(pos))

        self.settings_manager.settings["theme_button_scale"] = new_scale
        self.settings_manager.store_settings()

        self.theme_button_scale.label.config(text=new_scale)
        self.theme_button_scale.scale.config(value=new_scale)

    def __change_row_length(self, pos):
        self.change = True

        new_length = int(float(pos))

        self.settings_manager.settings["row_length"] = new_length
        self.settings_manager.store_settings()

        self.row_length.label.config(text=new_length)
        self.row_length.scale.config(value=new_length)

    def __change_font_size(self, pos):
        self.change = True

        new_size = int(float(pos))
        self.settings_manager.settings["font_size"] = new_size
        self.settings_manager.store_settings()

        self.font_size.label.config(text=new_size)
        self.font_size.scale.config(value=new_size)

    def __full_path_on_main(self, _):
        self.change = True
        self.settings_manager.settings["full_paths_main"] = (
            0 if self.settings_manager.settings["full_paths_main"] else 1
        )
        if self.settings_manager.settings["full_paths_main"]:
            self.full_path_on_main_check.config(
                image=self.image_manager.images["check_on"]
            )
        else:
            self.full_path_on_main_check.config(
                image=self.image_manager.images["check_off"]
            )
        self.settings_manager.store_settings()

    def __full_path_in_settings(self, _):
        self.change = True
        self.settings_manager.settings["full_paths_settings"] = (
            0 if self.settings_manager.settings["full_paths_settings"] else 1
        )
        if self.settings_manager.settings["full_paths_settings"]:
            self.full_path_in_settings_check.config(
                image=self.image_manager.images["check_on"]
            )
        else:
            self.full_path_in_settings_check.config(
                image=self.image_manager.images["check_off"]
            )
        self.settings_manager.store_settings()

    def __reset_settings(self):
        self.settings_manager.reset_to_defaults()
        self.tab_manager.update_all_tab_elements()

    def __change_color(self, index: int, name):
        self.change = True

        colors = [
            "bg_color",
            "sec_bg_color",
            "button_bg_color",
            "button_hov_color",
            "txt_color",
        ]

        color = colors[index]

        chosenColor = askcolor(
            self.settings_manager.settings[color], title="Choose " + name
        )[1]

        if chosenColor is None:
            return

        self.color_labels[index].config(bg=chosenColor)

        self.settings_manager.settings[color] = chosenColor
        self.settings_manager.store_settings()

        self.image_manager.load_images()
        self.update()

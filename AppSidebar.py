from customtkinter import *
from PIL import Image
import pathlib
import json


class Sidebar:
    sidebar_frame = None
    icons_path = pathlib.Path("Icons")
    icon_dict = {
        "youtube_button_icon_selected": CTkImage(
            Image.open(icons_path / "youtube_selected.png"), size=(32, 32)
        ),
        "youtube_button_icon_normal": CTkImage(
            Image.open(icons_path / "youtube_normal.png"), size=(32, 32)
        ),
        "explorer_button_icon_selected": CTkImage(
            Image.open(icons_path / "folder_selected.png"), size=(32, 32)
        ),
        "explorer_button_icon_normal": CTkImage(
            Image.open(icons_path / "folder_normal.png"), size=(32, 32)
        ),
    }
    with open(pathlib.Path("Data") / "button_settings.json", "r") as f:
        button_settings = json.load(f)

    invisible_grids = []

    def __init__(self, parent):
        self.parent = parent

        self.sidebar_frame = CTkFrame(master=self.parent.root)

        self.sidebar_frame.grid_rowconfigure((0, 1, 2), weight=1)

        file_explorer_button_config = self.button_settings["file_explorer_button"][
            "normal"
        ]
        youtube_installer_button_config = self.button_settings[
            "youtube_installer_button"
        ]["selected"]

        self.file_explorer_button = CTkButton(
            master=self.sidebar_frame,
            command=self.change_button_state,
            text="",
            width=40,
            height=50,
            border_width=2,
            corner_radius=0,
            hover_color="white",
            image=eval(file_explorer_button_config["image"]),
            fg_color=file_explorer_button_config["fg_color"],
            state=file_explorer_button_config["state"],
            border_color="#575757",
        )
        self.youtube_installer_button = CTkButton(
            master=self.sidebar_frame,
            text="",
            command=self.change_button_state,
            width=40,
            height=50,
            corner_radius=0,
            border_width=2,
            hover_color="white",
            border_color="#575757",
            state=youtube_installer_button_config["state"],
            fg_color=youtube_installer_button_config["fg_color"],
            image=eval(youtube_installer_button_config["image"]),
        )

        self.set_up()

    def set_up(self):
        self.sidebar_frame.grid(row=0, column=0, rowspan=4)
        self.file_explorer_button.grid(row=1, column=1)
        self.youtube_installer_button.grid(row=0, column=1)

    def change_button_state(self, state=[1]):
        youtube_installer_button_selected = self.button_settings[
            "youtube_installer_button"
        ]["selected"]
        youtube_installer_button_normal = self.button_settings[
            "youtube_installer_button"
        ]["normal"]
        file_explorer_button_selected = self.button_settings["file_explorer_button"][
            "selected"
        ]
        file_explorer_button_normal = self.button_settings["file_explorer_button"][
            "normal"
        ]

        if state[0] == 1:
            self.youtube_installer_button.configure(
                image=eval(youtube_installer_button_normal["image"]),
                fg_color=youtube_installer_button_normal["fg_color"],
                state=youtube_installer_button_normal["state"],
            )
            self.file_explorer_button.configure(
                image=eval(file_explorer_button_selected["image"]),
                fg_color=file_explorer_button_selected["fg_color"],
                state=file_explorer_button_selected["state"],
            )
            state[0] = 2
        else:
            self.youtube_installer_button.configure(
                image=eval(youtube_installer_button_selected["image"]),
                fg_color=youtube_installer_button_selected["fg_color"],
                state=youtube_installer_button_selected["state"],
            )
            self.file_explorer_button.configure(
                image=eval(file_explorer_button_normal["image"]),
                fg_color=file_explorer_button_normal["fg_color"],
                state=file_explorer_button_normal["state"],
            )
            state[0] = 1

        self.parent.switch_tabview()

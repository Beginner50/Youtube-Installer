import pathlib
from customtkinter import *
from PIL import Image
import subprocess


class FileButtonManager:
    layers = ["Downloads"]
    mode = "normal"
    current_layer = "Downloads"

    def __init__(self, parent, files_and_folders, **kwargs):
        self.file_buttons = []
        self.parent = parent

        for item in files_and_folders:
            self.file_buttons.append(
                FileButton(
                    self,
                    text=item["item_name"],
                    type=item["type"],
                    path=item["path"],
                    thumbnail=item["thumbnail"],
                    compound="top",
                    parent=item["parent"],
                    **kwargs,
                )
            )

    def traverse_deeper(self, next_layer):
        """Moves one layer downwards"""
        self.layers.append(next_layer)
        self.current_layer = next_layer
        self.remove_buttons()
        self.display_buttons()
        return pathlib.Path("\\".join(layer for layer in self.layers))

    def resurface(self):
        """Moves one layer upwards"""
        disable_back_button = False
        self.layers.pop()
        self.current_layer = self.layers[-1]
        self.remove_buttons()
        self.display_buttons()

        if len(self.layers) == 1:
            disable_back_button = True
        return disable_back_button, pathlib.Path(
            "\\".join(layer for layer in self.layers)
        )

    def refresh_file_buttons(self, file_button=None, **kwargs) -> None:
        # ---------------------------------------------------------------------------------
        def change_file_button_text(button, new_file_name) -> None:
            text = ""
            for i in range(len(new_file_name)):
                if i % 10 == 0 and i != 0:
                    text += "\n"
                text += new_file_name[i]
            button.configure(text=text)

        def rename_file_button_path(original_file_name, new_file_name):
            file_button.path = pathlib.Path(
                str(file_button.path).replace(original_file_name, new_file_name)
            )

        def rename_dependent_file_buttons(original_file_name, new_file_name):
            for button in self.file_buttons:
                if button.parent == original_file_name:
                    button.parent = new_file_name
                    button.path = file_button.path / button.text

        # ---------------------------------------------------------------------------------
        if self.mode == "moving":
            file_button.path = kwargs["new_path"]
            file_button.parent = str(kwargs["new_path"].parent).split("\\")[-1]
            file_button.state = "normal"
        elif self.mode == "rename":
            change_file_button_text(file_button, kwargs["new_file_name"])
            rename_file_button_path(
                kwargs["original_file_name"], kwargs["new_file_name"]
            )
            rename_dependent_file_buttons(
                kwargs["original_file_name"], kwargs["new_file_name"]
            )
            self.mode = "normal"

        if files_and_folders := kwargs.get("files_and_folders", False):
            file_button_names = [button.text for button in self.file_buttons]

            for file in files_and_folders:
                if file["item_name"] not in file_button_names:
                    self.file_buttons.append(
                        FileButton(
                            self,
                            master=self.parent.scrollable_frame,
                            single_click_event=self.parent.single_click_event,
                            double_click_event=self.parent.double_click_event,
                            on_select_color="coral1",
                            text=file["item_name"],
                            type=file["type"],
                            path=file["path"],
                            thumbnail=file["thumbnail"],
                            compound="top",
                            parent=file["parent"],
                        )
                    )

        if "moving" in kwargs:
            if kwargs["moving"]:
                self.mode = "moving"
                file_button.state = "being_moved"
                file_button.has_been_clicked = False
                file_button.configure(fg_color="transparent")
                file_button.grid_remove()
            else:
                self.mode = "normal"

        self.remove_buttons()
        self.display_buttons()

    def remove_buttons(self):
        """Hides all the file buttons"""
        [button.grid_forget() for button in self.file_buttons]

    def display_buttons(self):
        """Displays file buttons in the current layer"""
        current_file_buttons = list(
            filter(
                lambda file_button: True
                if (
                    file_button.parent == self.current_layer
                    and file_button.state == "normal"
                )
                else False,
                self.file_buttons,
            )
        )
        current_file_buttons = self.sort_buttons(current_file_buttons)

        row = -1
        for col, button in enumerate(current_file_buttons):
            if col % 4 == 0:
                row += 1
            button.grid(row=row, column=col % 4, padx=10)

    @staticmethod
    def sort_buttons(current_file_buttons):
        """Bubble sort for the file buttons (Folders appear before actual Files)"""

        ceiling = len(current_file_buttons) - 1
        swapped = True
        while swapped:
            swapped = False
            floor = 0
            while floor < ceiling:
                if current_file_buttons[floor] < current_file_buttons[floor + 1]:
                    container = current_file_buttons[floor + 1]
                    current_file_buttons[floor + 1] = current_file_buttons[floor]
                    current_file_buttons[floor] = container
                    swapped = True
                floor += 1
            ceiling -= 1
        return current_file_buttons

    def select_current_button(self, file_button, single_click_event):
        if not file_button.has_been_clicked:
            self._deselect_previous_button()
            file_button.has_been_clicked = True

            single_click_event(file_button)

            file_button.configure(fg_color=file_button.on_select_color)

    def _deselect_previous_button(self):
        for file_button in self.file_buttons:
            if file_button.has_been_clicked:
                file_button.configure(fg_color="transparent")
                file_button.has_been_clicked = False
                break


class FileButton(CTkButton):
    has_been_clicked = False
    state = "normal"

    def __init__(self, file_button_manager, **kwargs):
        self.file_button_manager = file_button_manager
        self.file_type = kwargs.pop("type")
        self.path = kwargs.pop("path")
        self.thumbnail = kwargs.pop("thumbnail")
        self.parent = kwargs.pop("parent")
        self.text = kwargs["text"]

        if len(kwargs["text"]) > 10:
            text = list(kwargs["text"])

            for index in range(len(text)):
                if index % 10 == 0 and index != 0:
                    text.insert(index, "\n")

            kwargs["text"] = "".join(char for char in text)

        if "width" not in kwargs.keys():
            kwargs.update({"width": 50})

        if "fg_color" not in kwargs.keys():
            kwargs.update({"fg_color": "transparent"})

        if "text_color" not in kwargs.keys():
            kwargs.update({"text_color": "black"})

        if "on_select_color" in kwargs.keys():
            self.on_select_color = kwargs.pop("on_select_color")
            kwargs.update({"hover_color": self.on_select_color})

        if "single_click_event" in kwargs.keys():
            self.single_click_event = kwargs.pop("single_click_event")

        if "double_click_event" in kwargs.keys():
            self.double_click_event = kwargs.pop("double_click_event")

        super().__init__(
            image=CTkImage(Image.open(self.thumbnail), size=(64, 64)),
            command=lambda: self.file_button_manager.select_current_button(
                self, self.single_click_event
            ),
            **kwargs,
        )
        self._canvas.bind("<Double-Button-1>", self.on_double_click)
        self._text_label.bind("<Double-Button-1>", self.on_double_click)
        self._image_label.bind("<Double-Button-1>", self.on_double_click)

    # noinspection PyUnusedLocal
    def on_double_click(self, e):
        if self.file_type == "FOLDER":
            self.has_been_clicked = False
            self.configure(fg_color="transparent")
            self.double_click_event(self.text, self.file_type)
        else:
            file = str(self.path).replace("%", " ")
            subprocess.Popen(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", file])

    def __repr__(self):
        return f"text:{self.text}, file_type:{self.file_type}, path:{self.path}, parent:{self.parent}"

    def __lt__(self, other):
        if self.file_type == "FILE" and other.file_type == "FOLDER":
            return True
        else:
            return False


class CustomDialog(CTkInputDialog):
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "button_fg_color": "IndianRed1",
                "button_hover_color": "IndianRed4",
                "button_text_color": "black",
            }
        )
        super().__init__(**kwargs)

    def _create_widgets(self):
        super()._create_widgets()
        try:
            self._cancel_button.configure(command=self._cancel_event)
        except AttributeError:
            pass

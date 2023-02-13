import pathlib
from customtkinter import *
import json
from PIL import Image
from CustomWidgets import CustomDialog
from tkinter import messagebox
import AppBackend


class ExplorerToolbar:
    cousin = None
    file_button_manager = None
    file_button_selected = None
    working_directory = pathlib.Path("Downloads")
    original_path, new_file_path = None, None
    mode = "normal"

    def __init__(self, parent):
        self.file_button_being_moved = None
        self.parent = parent

        self.explorer_toolbar_frame = CTkFrame(
            master=parent.explorer_frame, fg_color="white", height=50
        )

        self.explorer_toolbar_frame.grid_columnconfigure((0, 1), weight=1)

        self.back_button = CTkButton(
            master=self.explorer_toolbar_frame,
            text="Back",
            compound="top",
            width=40,
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
            image=CTkImage(Image.open("Icons/back-button.png"), size=(32, 32)),
        )
        self.back_button_replacement = CTkFrame(
            master=self.explorer_toolbar_frame,
            width=40,
            height=10,
            fg_color="transparent",
        )

        self.file_toolbar_frame = CTkFrame(
            master=self.explorer_toolbar_frame, fg_color="transparent", height=50
        )

        self.move_button = CTkButton(
            master=self.file_toolbar_frame,
            text="Move",
            compound="top",
            width=40,
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
            image=CTkImage(Image.open("Icons/move-button.png"), size=(32, 32)),
        )
        self.place_button = CTkButton(
            master=self.file_toolbar_frame,
            text="Place",
            width=40,
            image=CTkImage(Image.open("Icons/place_button.png"), size=(32, 32)),
            fg_color="transparent",
            text_color="black",
            compound="top",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
        )

        self.rename_button = CTkButton(
            master=self.file_toolbar_frame,
            text="Rename",
            compound="top",
            width=40,
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
            image=CTkImage(Image.open("Icons/rename-button.png"), size=(32, 32)),
        )
        self.cancel_button = CTkButton(
            master=self.file_toolbar_frame,
            text="Cancel",
            width=40,
            image=CTkImage(Image.open("Icons/cancel-button.png"), size=(32, 32)),
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            compound="top",
            font=CTkFont("Monospace", 12, "bold"),
        )

        self.delete_button = CTkButton(
            master=self.file_toolbar_frame,
            text="Delete",
            compound="top",
            width=40,
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
            image=CTkImage(Image.open("Icons/trash.png"), size=(32, 32)),
        )

        self.universal_tools_frame = CTkFrame(
            master=self.explorer_toolbar_frame,
            fg_color="transparent",
            height=50,
            border_width=3,
        )
        self.set_download_path_button = CTkButton(
            master=self.universal_tools_frame,
            text="Set Path",
            compound="top",
            width=40,
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
            image=CTkImage(Image.open("Icons/download.png"), size=(32, 32)),
        )
        self.create_folder_button = CTkButton(
            master=self.universal_tools_frame,
            text="Create Folder",
            compound="top",
            width=40,
            fg_color="transparent",
            text_color="black",
            hover_color="coral3",
            font=CTkFont("Monospace", 12, "bold"),
            image=CTkImage(Image.open("Icons/add-folder.png"), size=(32, 32)),
        )

    def set_up(self, cousin):
        self.cousin = cousin

        self.back_button.configure(command=self._click_back_button)
        self.move_button.configure(command=self._click_move_button)
        self.place_button.configure(command=self._click_place_button)
        self.cancel_button.configure(command=self._click_cancel_button)
        self.rename_button.configure(command=self._click_rename_button)
        self.delete_button.configure(command=self._click_delete_button)
        self.create_folder_button.configure(command=self._click_create_folder_button)
        self.set_download_path_button.configure(command=self._click_set_path_button)

        self.explorer_toolbar_frame.grid(row=1, column=0, columnspan=4, sticky="ew")
        self.back_button.grid(row=0, column=0, padx=3, sticky="w")
        self.back_button_replacement.grid(row=0, column=0, sticky="w")
        self.back_button.grid_remove()
        self.file_toolbar_frame.grid(row=0, column=1, sticky="ew")
        self.universal_tools_frame.grid(row=0, column=2, sticky="ew")

        for col, child in enumerate(self.universal_tools_frame.winfo_children()):
            if col == 0:
                child.grid(row=0, column=col, padx=12, sticky="e", pady=5)
            else:
                child.grid(row=0, column=col, sticky="e", pady=5)

    def show_toolbar(self) -> None:
        if self.file_button_manager.mode == "normal":
            widgets_to_be_placed = self.file_toolbar_frame.winfo_children()
            widgets_to_be_placed.remove(self.place_button)
            widgets_to_be_placed.remove(self.cancel_button)

            for col, child in enumerate(widgets_to_be_placed):
                child.grid(row=0, column=col, padx=5, sticky="w")

        elif self.file_button_manager.mode == "moving":
            [child.grid_remove() for child in self.file_toolbar_frame.winfo_children()]
            self.place_button.grid(row=0, column=0)
            self.cancel_button.grid(row=0, column=1)

    def hide_toolbar(self) -> None:
        for col, child in enumerate(self.file_toolbar_frame.winfo_children()):
            child.grid_remove()

    def _click_back_button(self) -> None:
        self.cousin.cruise_directory(direction="backward")

    def _click_move_button(self) -> None:
        self.file_button_being_moved = self.file_button_selected

        self.file_button_manager.refresh_file_buttons(
            file_button=self.file_button_being_moved, moving=True
        )
        self.show_toolbar()

    def _click_place_button(self) -> None:
        # Gets the original and new paths and move the file to its corresponding location
        self.original_path = self.file_button_being_moved.path
        self.new_file_path = self.working_directory / self.file_button_being_moved.text

        AppBackend.move_directory(self.original_path, self.new_file_path)

        # Displays the File Button in its new location
        self.hide_toolbar()
        self.file_button_manager.refresh_file_buttons(
            file_button=self.file_button_being_moved, new_path=self.new_file_path
        )

        # Alerts the program that the file button is no longer being moved
        self.file_button_manager.mode = "normal"
        self.file_button_being_moved = None

    def _click_cancel_button(self) -> None:
        # Alerts program file button is no longer being moved
        self.file_button_being_moved.state = "normal"
        self.file_button_being_moved = None

        # Refreshes the explorer tab
        self.file_button_manager.refresh_file_buttons(moving=False)
        self.hide_toolbar()

    def _click_rename_button(self) -> None:
        self.file_button_manager.mode = "rename"

        # Prompts user to enter new file name
        original_file_name = self.file_button_selected.text
        new_file_name = self.get_file_name(
            self.file_button_manager.file_buttons,
            text="Enter a new file name: ",
            title="Rename File",
        )

        # Renames file and refreshes display
        if new_file_name is None:
            return
        else:
            AppBackend.rename_directory(
                self.working_directory / original_file_name,
                self.working_directory / new_file_name,
                self.file_button_selected.thumbnail,
            )

            self.file_button_manager.refresh_file_buttons(
                file_button=self.file_button_selected,
                original_file_name=original_file_name,
                new_file_name=new_file_name,
            )

    def _click_create_folder_button(self):
        file_name = self.get_file_name(
            self.file_button_manager.file_buttons,
            text="Enter Folder name: ",
            title="Create Folder",
        )

        if file_name is None:
            return
        else:
            AppBackend.create_directory(self.working_directory / file_name)
            self.file_button_manager.refresh_file_buttons(
                files_and_folders=AppBackend.search_directory(reset=True)
            )

    def _click_delete_button(self):
        confirm_delete = messagebox.askyesno(
            title="Delete File", message="Confirm Delete File"
        )
        if confirm_delete:
            AppBackend.delete_directory(self.file_button_selected.path)

            self.file_button_selected.grid_forget()
            self.file_button_manager.file_buttons.remove(self.file_button_selected)
            self.file_button_selected = None

            self.hide_toolbar()

    def _click_set_path_button(self):
        if AppBackend.check_file_exists("Global_Settings.json"):
            with open(pathlib.Path("Data\\Global_Settings.json"), "r") as f:
                global_settings = json.load(f)

            global_settings["download_path"] = str(self.working_directory)

            with open(pathlib.Path("Data\\Global_Settings.json"), "w") as f:
                json.dump(global_settings, f, indent=2)
        else:
            with open(pathlib.Path("Data\\Global_Settings.json"), "w") as f:
                json.dump({"download_path": str(self.working_directory)}, f, indent=2)

        messagebox.showinfo(
            message=f"Download Path set to {self.working_directory}",
            title="Set Download Path",
        )

    @staticmethod
    def get_file_name(file_buttons, text=None, title=None) -> str:
        dialog = CustomDialog(text=text, title=title)
        new_name = dialog.get_input()
        new_name_original = new_name

        count = 0
        file_button_names = [button.text for button in file_buttons]
        while new_name in file_button_names:
            count += 1
            new_name = new_name_original + f"({count})"

        return new_name

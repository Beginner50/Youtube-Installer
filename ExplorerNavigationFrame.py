import pathlib
from CustomWidgets import FileButton, FileButtonManager
from customtkinter import *
import AppBackend


class ExplorerNavigationFrame:
    working_path: pathlib.Path
    file_button_manager: FileButtonManager = None
    is_button_selected: bool = False
    cousin = None

    def __init__(self, parent):
        self.parent = parent

        self.file_navigation_frame = CTkFrame(
            master=parent.explorer_frame,
            fg_color="cornsilk",
            corner_radius=4,
            border_width=3,
        )

        self.file_navigation_frame.grid_rowconfigure(0, weight=1)
        self.file_navigation_frame.grid_columnconfigure(0, weight=1)

        # Canvas + Scrollbar
        self.file_navigation_canvas = CTkCanvas(
            master=self.file_navigation_frame, background="cornsilk"
        )
        self.scrollbar = CTkScrollbar(
            master=self.file_navigation_frame, command=self.file_navigation_canvas.yview
        )

        # Scrollable Frame                      (Frame inside Canvas)
        self.scrollable_frame = CTkFrame(
            master=self.file_navigation_canvas, fg_color="cornsilk"
        )
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.file_navigation_canvas.configure(
                scrollregion=self.file_navigation_canvas.bbox("all")
            ),
        )

        self.file_navigation_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.file_navigation_canvas.configure(yscrollcommand=self.scrollbar.set)

    def set_up(self, cousin) -> None:
        self.cousin = cousin

        self.file_navigation_frame.grid(row=2, column=1, columnspan=3, sticky="nsew")
        self.file_navigation_canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

    def initialise_files_and_folders(self) -> None:
        files_and_folders = AppBackend.search_directory()
        self.file_button_manager = FileButtonManager(
            self,
            files_and_folders,
            master=self.scrollable_frame,
            single_click_event=self.single_click_event,
            double_click_event=self.double_click_event,
            on_select_color="coral1",
        )
        self.cousin.file_button_manager = self.file_button_manager

    def display_files_and_folders(self) -> None:
        self.file_button_manager.remove_buttons()
        self.file_button_manager.display_buttons()

    def single_click_event(self, file_button: FileButton) -> None:
        """Returns the button object and shows toolbar when a file button has been clicked once"""
        self.cousin.file_button_selected = file_button
        self.cousin.show_toolbar()

    def double_click_event(self, filename: str, file_type: str) -> None:
        if file_type == "FOLDER":
            self.cruise_directory(direction="forward", filename=filename)

    def cruise_directory(self, direction: str, filename: str = None) -> None:
        if direction == "forward":
            self.cousin.working_directory = self.file_button_manager.traverse_deeper(
                filename
            )

            self.cousin.back_button_replacement.grid_remove()
            self.cousin.back_button.grid()

            self.cousin.hide_toolbar()
            if self.file_button_manager.mode == "moving":
                self.cousin.show_toolbar()

        elif direction == "backward":
            self.cousin.hide_toolbar()
            if self.file_button_manager.mode == "moving":
                self.cousin.show_toolbar()
            (
                disable_back_button,
                self.cousin.working_directory,
            ) = self.file_button_manager.resurface()

            if disable_back_button:
                self.cousin.back_button.grid_remove()
                self.cousin.back_button_replacement.grid()

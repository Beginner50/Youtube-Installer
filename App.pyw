import pathlib
import subprocess
import sys

if 'YtVenv' not in str(sys.executable):
    try:
        subprocess.Popen([str(pathlib.Path('YtVenv\\Scripts\\python.exe')), 'App.pyw'])
    except FileNotFoundError:
        subprocess.run(['python', '-m', 'venv', 'YtVenv'])
        subprocess.run([str(pathlib.Path('YtVenv\\Scripts\\python.exe')), '-m', 'pip', 'install', '-r', 'requirements.txt'])
        subprocess.Popen([str(pathlib.Path('YtVenv\\Scripts\\python.exe')), 'App.pyw'])
    sys.exit()

from customtkinter import *
import AppBackend
from InstallerSearchFrame import SearchFrame
from AppSidebar import Sidebar
from ExplorerToolbar import ExplorerToolbar
from ExplorerNavigationFrame import ExplorerNavigationFrame


class GUI:
    search_frame, sidebar, explorer_toolbar, explorer_navigation_frame = (
        None,
        None,
        None,
        None,
    )
    (
        youtube_logo_frame,
        youtube_installer_logo,
        explorer_logo_frame,
        file_explorer_logo,
    ) = (None, None, None, None)
    installer_frame, explorer_frame, explorer_side_frame = None, None, None
    download_warning = None
    invisible_frames = []

    state = 1
    download_path = pathlib.Path("Downloads")

    def __init__(self):
        self.root = CTk()

        self.root.geometry("450x450")
        self.root.title("Youtube Installer")
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.create_file_explorer_frame()
        self.file_explorer_frame_set_up()

        self.create_youtube_installer_frame()
        self.youtube_installer_frame_set_up()

        self.sidebar = Sidebar(self)

    def create_youtube_installer_frame(self):
        """Creates the main tab:- YouTube Installer Tab"""

        # Creating the YouTube installer tabview
        self.installer_frame = CTkFrame(master=self.root, fg_color="antique white")
        self.installer_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.installer_frame.columnconfigure((1, 2), weight=1)
        self.installer_frame.rowconfigure(3, weight=1)

        # Setting up the widgets in the installer tab
        self.youtube_logo_frame = CTkFrame(
            master=self.installer_frame,
            fg_color="AntiqueWhite2",
            border_width=2,
            corner_radius=0,
        )

        self.youtube_installer_logo = CTkLabel(
            master=self.youtube_logo_frame,
            text="Youtube Downloader",
            text_color="firebrick1",
            font=CTkFont("Comic Sans", 30, "bold"),
        )
        self.download_warning = CTkLabel(
            master=self.installer_frame, text="", font=("Adobe Garamond", 18)
        )

        self.search_frame = SearchFrame(self)

    def create_file_explorer_frame(self):
        """Creates the second tab:- File Explorer Tab"""

        # Creating the File explorer tabview
        self.explorer_frame = CTkFrame(master=self.root, fg_color="antique white")

        self.explorer_frame.columnconfigure((1, 2), weight=1)
        self.explorer_frame.rowconfigure(2, weight=1)

        # Setting up the widgets in the explorer tab
        self.explorer_logo_frame = CTkFrame(
            master=self.explorer_frame,
            fg_color="AntiqueWhite2",
            border_width=2,
            corner_radius=0,
        )
        self.file_explorer_logo = CTkLabel(
            master=self.explorer_logo_frame,
            text="File Explorer",
            text_color="firebrick1",
            font=CTkFont("Comic Sans", 30, "bold"),
        )
        self.explorer_side_frame = CTkFrame(
            master=self.explorer_frame,
            fg_color="AntiqueWhite2",
            width=25,
            corner_radius=0,
        )

        self.explorer_toolbar = ExplorerToolbar(self)
        self.explorer_navigation_frame = ExplorerNavigationFrame(self)
        self.explorer_toolbar.set_up(self.explorer_navigation_frame)
        self.explorer_navigation_frame.set_up(self.explorer_toolbar)

    def file_explorer_frame_set_up(self) -> None:
        self.explorer_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.explorer_logo_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.file_explorer_logo.grid(row=0, column=0, padx=138, pady=3)

        self.explorer_side_frame.grid(row=2, column=0, sticky="ns")

        self.explorer_navigation_frame.initialise_files_and_folders()
        self.explorer_navigation_frame.display_files_and_folders()
        self.explorer_frame.grid_remove()

    def youtube_installer_frame_set_up(self) -> None:
        """Placing the installer tab on the window and setting up the search tab"""

        def place_invisible_frames():
            for i, col in enumerate((0, 3)):
                self.invisible_frames.append(
                    CTkFrame(
                        master=self.installer_frame, width=95, fg_color="transparent"
                    )
                )
                self.invisible_frames[i].grid(row=2, column=col, rowspan=3, sticky="ns")

        self.youtube_logo_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.youtube_installer_logo.grid(row=0, column=0, padx=80, pady=3)
        self.download_warning.grid(row=4, column=1, columnspan=2, pady=20)

        place_invisible_frames()

    def switch_tabview(self):
        if self.state == 1:
            self.installer_frame.grid_remove()
            self.explorer_navigation_frame.file_button_manager.refresh_file_buttons(
                files_and_folders=AppBackend.search_directory(reset=True)
            )
            self.explorer_frame.grid()

            self.state = 2
        else:
            self.installer_frame.grid()
            self.explorer_frame.grid_remove()

            self.state = 1


if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()

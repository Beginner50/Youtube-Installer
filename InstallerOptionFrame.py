from customtkinter import *
from InstallerDownloadFrame import DownloadFrame


class OptionFrame:
    invisible_grids = []
    radio_buttons = []
    resolution_dict = {}

    def __init__(self, parent, grandparent, radio_var):
        """ Grandparent - YoutubeInstaller/GUI, Parent - SearchFrame"""
        self.radio_var = radio_var
        self.parent = parent
        self.grandparent = grandparent

        self.option_frame = CTkFrame(
            master=grandparent.installer_frame, border_width=2, fg_color="NavajoWhite"
        )
        self.option_frame.grid(row=3, column=1, columnspan=2, sticky="nsew", pady=10)

        self.option_frame.grid_rowconfigure(4, weight=1)
        self.option_frame.grid_columnconfigure((0, 1, 2), weight=1)

        for i, col in enumerate((0, 3)):
            self.invisible_grids.append(
                CTkFrame(master=self.option_frame, width=10, fg_color="transparent")
            )
            self.invisible_grids[i].grid(row=0, column=col, rowspan=4, padx=5, pady=4)

        self.download_frame = DownloadFrame(self, parent, grandparent)

    def set_up(self, resolution_dict, streams):
        self.resolution_dict = resolution_dict
        self.generate_radios()
        self.download_frame.set_up(streams)

    def reset_option_frame(self):
        [radio_button.destroy() for radio_button in self.radio_buttons]
        self.radio_buttons = []
        self.grandparent.download_warning.configure(text="")

        self.download_frame.reset()

    def generate_radios(self):
        col, row = 0, 0
        for quality, itag in self.resolution_dict.items():
            text_color = 'DarkRed' if 'kbps' in quality else 'SpringGreen4'

            self.radio_buttons.append(CTkRadioButton(
                master=self.option_frame,
                variable=self.radio_var,
                value=f'{itag} {quality}',
                text=quality,
                text_color=text_color,
            ))

            col += 1
            if col == 3:
                col = 1
                row += 1

            if col == 1:
                self.radio_buttons[-1].grid(row=row, column=col, padx=30)
                continue
            self.radio_buttons[-1].grid(row=row, column=col, pady=5)

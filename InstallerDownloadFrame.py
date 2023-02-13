import multiprocessing
import time
from customtkinter import *
import AppBackend


class DownloadFrame:
    download_stream_thread = None
    streams = None

    def __init__(self, parent, grandparent, grandparentx2):
        self.grandparentx2 = grandparentx2
        self.grandparent = grandparent
        self.parent = parent

        self.download_frame = CTkFrame(
            master=parent.option_frame, fg_color="transparent"
        )
        self.download_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.download_button = CTkButton(
            master=self.download_frame,
            text="Download",
            text_color='black',
            command=self.on_download_button_click,
            fg_color="IndianRed1",
            hover_color="IndianRed4",
        )

    def set_up(self, streams):
        self.download_frame.grid(
            row=4, column=1, columnspan=2, padx=5, pady=5, sticky="nsew"
        )
        self.download_button.grid(row=0, column=1)
        self.streams = streams

    def reset(self):
        self.download_button.grid_forget()
        self.download_frame.grid_forget()

    def on_download_button_click(self):
        itag, quality = self.parent.radio_var.get().split(' ')
        self.download_stream(quality, int(itag))

    @AppBackend.multithread_task
    def download_stream(self, quality, itag):
        sentinel = multiprocessing.Value("i", 0)
        download_stream_process = multiprocessing.Process(
            target=AppBackend.download_stream, args=(itag, self.streams, sentinel)
        )
        download_stream_process.start()

        self.play_loading_animation(sentinel, quality)
        self.grandparentx2.download_warning.configure(
            text=f"Downloaded {quality}", text_color="LightSeaGreen"
        )

        download_stream_process.join()

    def play_loading_animation(self, sentinel, quality):
        count = 0
        placeholder_text = (
            f"Downloading {quality}.",
            f"Downloading {quality}..",
            f"Downloading {quality}...",
        )

        while sentinel.value == 0:
            time.sleep(1)
            self.grandparentx2.download_warning.configure(
                text_color="DarkOrchid", text=f"{placeholder_text[count % 3]}"
            )
            count += 1

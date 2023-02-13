import multiprocessing
import time
from customtkinter import *
import re
import AppBackend
import http.client
from InstallerOptionFrame import OptionFrame


class SearchFrame:
    previous_search = None
    acquire_stream_thread = None
    streams = []

    def __init__(self, parent):
        self.parent = parent

        self.search_bar = CTkEntry(master=self.parent.installer_frame
                                   , placeholder_text='Enter Url here'
                                   , width=300)
        self.search_button = CTkButton(master=self.parent.installer_frame, text='search'
                                       , font=('Roboto', 16)
                                       , width=60
                                       , fg_color='IndianRed1'
                                       , hover_color='IndianRed4'
                                       , text_color='black'
                                       , command=self.on_search_button_click)
        self.warning_label = CTkLabel(master=self.parent.installer_frame
                                      , text=''
                                      , font=('Adobe Garamond', 18))

        self.set_up()
        self.option_frame = OptionFrame(self, parent, StringVar())

    def set_up(self):
        self.search_bar.grid(row=1, column=0, columnspan=3
                             , pady=10, padx=10)
        self.search_button.grid(row=1, column=3)
        self.warning_label.grid(row=2, column=1, columnspan=2)

    def on_search_button_click(self):
        current_search = self.search_bar.get()
        if self.previous_search is not None and self.previous_search != current_search:
            self.option_frame.reset_option_frame()

        url_regex = re.compile(r'^https://www.youtube.com/watch')
        is_valid = False if url_regex.search(current_search) is None else True

        if current_search != '' and is_valid:
            if self.previous_search is None or current_search != self.previous_search:
                self.previous_search = current_search
                self.get_streams(current_search)
        elif current_search != '':
            self.warning_label.configure(text_color='red', text='Invalid URL Entered')

    @AppBackend.multithread_task
    def get_streams(self, url):
        sentinel = multiprocessing.Value('i', 0)
        container = multiprocessing.Queue()
        get_stream_process = multiprocessing.Process(target=AppBackend.get_streams, args=(container, url, sentinel))
        get_stream_process.start()

        self.play_loading_animation(sentinel)

        if sentinel.value == 2:
            self.warning_label.configure(text_color='red', text='Invalid URL Entered')
            return
        elif sentinel.value == 3:
            self.warning_label.configure(text_color='red', text='Failed To Acquire Streams')

        self.streams = container.get()
        get_stream_process.join()
        resolution_dict = AppBackend.filter_streams(self.streams)

        self.warning_label.configure(text='Streams Acquired', text_color='LightSeaGreen')

        self.option_frame.set_up(resolution_dict, self.streams)

    def play_loading_animation(self, sentinel):
        count = 0
        placeholder_text = ('Acquiring Streams.', 'Acquiring Streams..', 'Acquiring Streams...')
        while sentinel.value == 0:
            try:
                time.sleep(1)
                self.warning_label.configure(text_color='DarkOrchid', text=f'{placeholder_text[count % 3]}')
                count += 1
            except http.client.IncompleteRead:
                sentinel.value = 3
                break

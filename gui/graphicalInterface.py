# @Author: Debora Stuck
# @Time: 06.2022

from tkinter import *
from src.frame import Frame
from src.gifEventFrame import GifEventFrame


class GraphicalInterface:

    def __init__(self):
        window = Tk()
        window.title("Video Frame")
        window.geometry("500x320")

        text_orientation_title = Label(window, justify="left", font=("Arial", 12), fg='#00f',
                                       text="Fill in the inputs and click on one option to generate video frames")
        text_orientation_title.place(x=10, y=10)
        text_orientation = Label(window, justify="left",
                                 text="*No field is required. \n"
                                      "*If don't pass the path, the directory where this .exe was saved will be used."
                                      "\n*If don't pass the other fields, the default value will be used")
        text_orientation.place(x=10, y=40)

        self.response_text = Label(window, text="")
        self.response_text.place(x=50, y=280)

        input_path_label = Label(window, justify="left", text="Path to search videos/annotations")
        input_path_label.place(x=10, y=100)
        self.input_path_text = Entry(window)
        self.input_path_text.place(x=250, y=100)

        input_seconds_before_label = Label(window, justify="left", text="Seconds Before")
        input_seconds_before_label.place(x=10, y=130)
        self.input_seconds_before_text = Entry(window)
        self.input_seconds_before_text.insert(0, "0")
        self.input_seconds_before_text.place(x=250, y=130)

        input_seconds_after_label = Label(window, justify="left", text="Seconds After")
        input_seconds_after_label.place(x=10, y=160)
        self.input_seconds_after_text = Entry(window)
        self.input_seconds_after_text.insert(0, "5")
        self.input_seconds_after_text.place(x=250, y=160)

        input_video_extension_label = Label(window, justify="left", text="Video Extension")
        input_video_extension_label.place(x=10, y=190)
        self.input_video_extension_text = Entry(window)
        self.input_video_extension_text.insert(0, ".mkv")
        self.input_video_extension_text.place(x=250, y=190)

        frame_button = Button(window, text="Create frames", command=self.call_create_frame)
        frame_button.place(x=10, y=230)

        event_frame_button = Button(window, text="Create event frames", command=self.call_create_event_frame)
        event_frame_button.place(x=145, y=230)

        gif_button = Button(window, text="Create gifs", command=self.call_create_gif)
        gif_button.place(x=305, y=230)

        cancel_button = Button(window, text="Cancel", command=window.destroy)
        cancel_button.place(x=400, y=280)

        window.mainloop()

    def print_response(self, response):
        if response == "Success!":
            self.response_text.config(fg='#008000')
        else:
            self.response_text.config(fg='#f00')
        self.response_text["text"] = response

    def call_create_frame(self):
        path_text = self.input_path_text.get()
        video_ext = self.input_video_extension_text.get()
        vf = Frame(video_ext, path_text)
        response = vf.create_frame()
        self.print_response(response)

    def call_create_gif(self):
        path_text = self.input_path_text.get()
        video_ext = self.input_video_extension_text.get()
        seconds_before = self.input_seconds_before_text.get()
        seconds_after = self.input_seconds_after_text.get()
        vf = GifEventFrame(video_ext, path_text, seconds_before, seconds_after, "GIF")
        response = vf.create_gif_event_frame()
        self.print_response(response)

    def call_create_event_frame(self):
        path_text = self.input_path_text.get()
        video_ext = self.input_video_extension_text.get()
        vf = GifEventFrame(video_ext, path_text, "", "", "EVENT_FRAME")
        response = vf.create_gif_event_frame()
        self.print_response(response)






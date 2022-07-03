# @Author: Debora Stuck
# @Time: 06.2022

import cv2
import json
import os
import sys
from pathlib import Path
from src.globLabelVideo import GlobLabelVideo


class GifEventFrame:

    def __init__(self, video_ext, search_in_path, sec_start, sec_end, action):
        """
       Initializes the class with the specific params, but the user can send other values in the graphical interface
       :param video_ext: String
       :param search_in_path: String
       """
        self.dir_event_frame = 'eventFrames/'
        self.annotation_extension = '.json'
        if video_ext == "":
            self.video_extension = ".mkv"
        else:
            self.video_extension = video_ext
        if search_in_path != "":
            self.search_in_path = search_in_path
        elif getattr(sys, 'frozen', False):
            self.search_in_path = os.path.dirname(sys.executable)
        else:
            self.search_in_path = str(Path(__file__).parents[2])
        self.action = action
        if sec_start == "":
            self.sec_start = 0
        else:
            self.sec_start = sec_start
        if sec_end == "":
            self.sec_end = 5
        else:
            self.sec_end = sec_end
        self.g = GlobLabelVideo()

    def create_gif_event_frame(self):
        """
        Base method, calls the other methods to create the parts of the video (gifs) or the event frames
        The glob will search for files with annotation extension in the subfolders of the base directory
        Checks if the annotation extension is .json before continue
        Call the globLabel method to get the list of directories with annotations files and
        the new directory to save the frames
        Call the save_gif_event_frame method
        :return String (success or error)
        """
        directory = self.search_in_path + '/**/*' + self.annotation_extension
        if os.path.exists(self.search_in_path):
            if self.annotation_extension == '.json':
                label_files, new_dir_gif = self.g.glob_label(directory)
            else:
                return 'Error: the file extension must be json'
        else:
            return 'Error: this directory does not exist'
        response = self.save_gif_event_frame(label_files, new_dir_gif)
        return response

    def save_gif_event_frame(self, label_files, new_dir_gif):
        """
        For all annotations files found, define the dictionary from JSON object
        Iterating through the json list
        The glob will search for files with video extension in the subfolders of the base directory
        For all video files found, capture the video with OpenCV
        For all annotations, checks if the first character from gameTime annotation
        is the same as the first character from video file name
        Get the minute and the second of gameTime annotation
        Define the number of the start frame and the end frame, multiplying by fps (frames per second)
        If the user click on the gif button in the graphical interface, call the save_gif method
        If the user click on the event frame button in the graphical interface, call the save_event_frame method
        :param label_files: String (the directory with annotations file)
        :param new_dir_gif: String
        :return String (success or error)
        """
        response = "Success1"
        for file_path in label_files:
            json_file = open(file_path)
            data = json.load(json_file)
            dict_annotation = []

            for i in data['annotations']:
                dict_annotation.append(i)

            json_file.close()
            path = os.path.dirname(file_path)
            video_directory = self.search_in_path + '/**/*' + self.video_extension
            video_files, new_dir_video = self.g.glob_video(video_directory)

            for video_file in video_files:
                video_name = os.path.basename(Path(video_file).stem)
                cap = cv2.VideoCapture(video_file)
                fps = cap.get(cv2.CAP_PROP_FPS)
                parts = []
                label = []

                for a in dict_annotation:
                    if a['gameTime'][:1] == video_name[:1]:
                        label.append(a['label'])
                        minutes = a['gameTime'][4:-3]
                        seconds = a['gameTime'][-2:]
                        total_seconds = int(60 * int(minutes) + int(seconds))
                        frame_start = ((total_seconds + int(self.sec_start)) * fps)
                        frame_end = ((total_seconds + int(self.sec_end)) * fps)
                        if frame_start != 0:
                            frame_start = frame_start - 1
                        parts.append((frame_start, frame_end))

                if self.action == "EVENT_FRAME":
                    response = self.save_event_frame(path, parts, label, video_name, cap)
                elif self.action == "GIF":
                    response = self.save_gif(cap, parts, label, video_name, new_dir_gif)
                else:
                    return "Could not identify the action. Try again!"
        return response

    def save_gif(self, cap, parts, label, video_name, new_dir_gif):
        """
        Create and save the parts of the video (gifs)
        Read the video
        Define the fourcc for windows
        Save the parts of video in new directory with the name consisting of:
        label name + video name + start frame number + end frame number
        :param cap: video capture object from OpenCV
        :param parts: list (the frame numbers of the annotations)
        :param label: list (the label names of the annotations)
        :param video_name: String
        :param new_dir_gif: String (path to save gifs)
        :return String (success or error)
        """
        ret, frame = cap.read()
        h, w, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writers = []

        for index, frame_number in enumerate(parts):
            start, end = frame_number
            writers.append(cv2.VideoWriter
                           (f"{new_dir_gif}/{label[index]}-{video_name}-{start}-{end}{self.video_extension}",
                            fourcc, 25.0, (w, h)))

        f = 0
        while ret:
            f += 1
            for i, part in enumerate(parts):
                start, end = part
                if start <= f <= end:
                    writers[i].write(frame)
            ret, frame = cap.read()

        for writer in writers:
            writer.release()

        cap.release()
        return "Success!"

    def save_event_frame(self, path, parts, label, video_name, cap):
        """
        Create and save the event frames
        Define the name of the new directory
        Checks if the new directory exists before creating it
        id_frame has two numbers: the frame to start and to end
        Use id_start as the frame you want
        Read the frame
        Save the frame in new directory with the name consisting of: label name + video name + frame number
        :param path: String (the directory with annotations file)
        :param parts: list (the frame numbers of the annotations)
        :param label: list (the label names of the annotations)
        :param video_name: String
        :param cap: video capture object from OpenCV
        :return String (success or error)
        """
        new_dir_event_frame = path + '/' + self.dir_event_frame
        try:
            if not os.path.exists(new_dir_event_frame):
                os.mkdir(new_dir_event_frame)
        except OSError:
            return 'Error: creating directory of data'

        for index, id_frame in enumerate(parts):
            id_start, id_end = id_frame
            cap.set(1, id_start)
            ret, frame = cap.read()
            cv2.imwrite(f'{new_dir_event_frame}{label[index]}-{video_name}-{id_start}.jpg', frame)

        return "Success!"





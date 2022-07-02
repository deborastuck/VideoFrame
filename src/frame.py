# @Author: Debora Stuck
# @Time: 06.2022

import pathlib
import cv2
import os
from pathlib import Path
from src.globLabelVideo import GlobLabelVideo


class Frame:

    def __init__(self, video_ext, search_in_path):
        """
       Initializes the class with the specific params, but the user can send other values in the graphical interface
       :param video_ext: String
       :param search_in_path: String (the default value is where the executable was saved)
       """
        self.dir_frame = 'frames/'
        self.annotation_extension = '.json'
        if video_ext == "":
            self.video_extension = '.mkv'
        else:
            self.video_extension = video_ext
        if search_in_path == "":
            self.search_in_path = str(pathlib.Path(__file__).parents[2])
        else:
            self.search_in_path = search_in_path
        self.g = GlobLabelVideo()

    def create_frame(self):
        """
        Base method, calls the other methods to create the video frames
        The glob will search for files with video extension in the subfolders of the base directory
        Call the save_frame method
        :return String (success or error)
        """
        directory = self.search_in_path + '/**/*' + self.video_extension
        if os.path.exists(self.search_in_path):
            video_files, new_dir_video = self.g.glob_video(directory)
        else:
            return 'Error: this directory does not exist'

        response = self.save_frame(video_files, new_dir_video)
        return response

    def save_frame(self, video_files, new_dir):
        """
        For all video files found, get the file name
        Capture the video with OpenCV
        While ret is true, read the video getting the boolean value (ret) and the frame image
        Save the frame image in new directory with the name consisting of:
        frame + file name + number of the current frame sequence + extension jpg
        :param video_files: list
        :param new_dir: String
        :return String (success or error)
        """
        for path in video_files:
            filename = os.path.basename(Path(path).stem)
            cam = cv2.VideoCapture(path)
            currentframe = 0

            while True:
                ret, frame = cam.read()
                if ret:
                    name = new_dir + '/frame' + filename + str(currentframe) + '.jpg'
                    cv2.imwrite(name, frame)
                    currentframe += 1
                else:
                    break

            cam.release()
            cv2.destroyAllWindows()

        return "Success!"








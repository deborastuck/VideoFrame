# @Author: Debora Stuck
# @Time: 06.2022

import glob
import os


class GlobLabelVideo:

    def __init__(self):
        self.dir_frame = 'frames/'
        self.dir_gif = 'gifs/'

    def glob_label(self, directory):
        """
        Search annotations files in base directory
        Uses glob which returns the files that match the directory specified in the argument and the extension file
        Checks if the annotations file directory exists before continuing
        Define the name of the new directory
        Checks if the new directory exists before creating it
        Save the directory of all found files
        :param directory: String
        :return list (label_files) and String (new_dir_gif)
        """
        new_dir_gif = ""
        label_files = []
        for path in glob.glob(directory):
            if os.path.exists(path):
                new_dir_gif = os.path.dirname(path) + "/" + self.dir_gif
                try:
                    if not os.path.exists(new_dir_gif):
                        os.mkdir(new_dir_gif)
                    label_files.append(path)
                except OSError:
                    return 'Error: creating directory of data'
            else:
                return 'Error: this directory does not exist'
        return label_files, new_dir_gif

    def glob_video(self, directory):
        """
        Search video files in base directory
        Uses glob which returns the files that match the directory specified in the argument and the extension file
        Define the name of the new directory
        Checks if the new directory exists before creating it
        Save the directory of all found files
        :param directory: String
        :return list video_files and String new_dir_video
        """
        video_files = []
        new_dir_video = ""
        for path in glob.glob(directory):
            if os.path.exists(path):
                new_dir_video = os.path.dirname(path) + '/' + self.dir_frame
                try:
                    if not os.path.exists(new_dir_video):
                        os.mkdir(new_dir_video)
                    video_files.append(path)
                except OSError:
                    return 'Error: creating directory of data'
            else:
                return 'Error: this directory does not exist'
        return video_files, new_dir_video










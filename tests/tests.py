# @Author: Debora Stuck
# @Time: 06.2022

import pathlib
import unittest
import os
import sys
import glob
import logging
from src.frame import Frame
from src.gifEventFrame import GifEventFrame


class Tests(unittest.TestCase):

    def test_error_directory(self):
        """
        Checks if directory exists
        :return: Error
        """
        vf = Frame('.mkv', 'test')
        result = vf.create_frame()
        expected = 'Error: this directory does not exist'
        log = logging.getLogger("Testing directory")
        log.debug("sent path: test")
        log.debug("return message: Error: this directory does not exist")
        self.assertEqual(result, expected)

    def test_create_frame(self):
        """
        Checks if create frames in path
        :return: True
        """
        directory = self.get_directory("frames")
        number_files = self.get_number_files(directory[0])
        vf = Frame('.mkv', '')
        vf.create_frame()
        number_frames = self.get_number_files(directory[0])
        log = logging.getLogger("Testing frames")
        log.debug("files before create frames= %r", number_files)
        log.debug("files after create frames= %r", number_frames)
        self.assertTrue(number_files < number_frames)

    def test_create_gif(self):
        """
        Checks if create gifs in path
        :return: True
        """
        directory = self.get_directory("gifs")
        number_files = self.get_number_files(directory[0])
        gef = GifEventFrame('.mkv', '', '', '', "GIF")
        gef.create_gif_event_frame()
        number_gifs = self.get_number_files(directory[0])
        log = logging.getLogger("Testing gifs")
        log.debug("files before create gifs= %r", number_files)
        log.debug("files after create gifs= %r", number_gifs)
        self.assertTrue(number_files < number_gifs)

    def test_create_event_frame(self):
        """
        Checks if create event frames in path
        :return: True
        """
        directory = self.get_directory("eventFrames")
        number_files = self.get_number_files(directory[0])
        gef = GifEventFrame('.mkv', '', '', '', "EVENT_FRAME")
        gef.create_gif_event_frame()
        number_event_frames = self.get_number_files(directory[0])
        log = logging.getLogger("Testing event_frames")
        log.debug("files before create event_frames= %r", number_files)
        log.debug("files after create event_frames= %r", number_event_frames)
        self.assertTrue(number_files < number_event_frames)

    def get_directory(self, path):
        """
        Get the directory with wanted files
        :return: String
        """
        directory = glob.glob(str(pathlib.Path(__file__).parents[2]) + '/**/' + path)
        return directory

    def get_number_files(self, directory):
        """
        Get the number of files found
        :return: int
        """
        list_files = os.listdir(directory)
        number_files = len(list_files)
        return number_files

    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Testing directory").setLevel(logging.DEBUG)
    logging.getLogger("Testing frames").setLevel(logging.DEBUG)
    logging.getLogger("Testing gifs").setLevel(logging.DEBUG)
    logging.getLogger("Testing event_frames").setLevel(logging.DEBUG)
    unittest.main(argv=[''], verbosity=2, exit=False)


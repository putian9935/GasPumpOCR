import cv2
import time
from time import perf_counter, sleep
import sys

from matplotlib.pyplot import get
from logger import Logger
from takeAndroidScreenshot import takeScreenshot

from ImageProcessing import FrameProcessor

from color_classification import ColorClassification
from pre_process import preprocessing
from datetime import timedelta


def getDigits():
    """Get digit string from raw picture"""

    version = '_2_0'
    std_height = 90
    roi = [673, 375, 987, 534]
    rot_angle = 2

    frameProcessor = FrameProcessor(std_height, version)
    def preprocessor(_): return preprocessing(_, roi, rot_angle)

    def process_func(file_name):
        frameProcessor.set_image(file_name, preprocessor)
        output = frameProcessor.process_image_plain(
            ColorClassification().convert_to_01)
        return output
    return process_func


class Reader:
    def __init__(self, initial_exponent, screenshot_buffer, sleep_init=1):
        self.exponent = initial_exponent
        self.logger = Logger()
        self.sleep_factor = 1.1
        self.sleep_lag = sleep_init
        self.screenshot_buffer = screenshot_buffer
        self.get_digit = getDigits()

    def turn_on_read(self):
        last_digits = None
        while True:
            takeScreenshot(self.screenshot_buffer)
            new_digits = self.get_digit(self.screenshot_buffer)

            if new_digits == last_digits:
                self.sleep_lag *= self.sleep_factor
            else:
                pressure = self.cast_digits_to_number(last_digits, new_digits)
                print('-'*81)
                print("New pressure of %s since %s elapsed, " % (
                    pressure,
                    str(timedelta(seconds=perf_counter()))
                ))
                print("Current sleep lag is %d s" % int(self.sleep_lag))
                print('-'*81)
                self.logger.log([perf_counter(), pressure])
                last_digits = new_digits
            sleep(self.sleep_lag)

    def cast_digits_to_number(self, old_digits, new_digits):
        """Given new and last digits, return the correct value
        """
        old = int(old_digits)
        new = int(new_digits)
        if abs(new - old) > 500:
            self.exponent -= 1
        return new * 10 ** self.exponent


reader = Reader(-5, "./1.png")
reader.turn_on_read()

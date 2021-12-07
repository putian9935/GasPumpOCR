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

def getDigits():
    """Get digit string from raw picture"""

    version = '_2_0'
    std_height = 90
    roi = [529, 672, 701, 999]
    rot_angle = 2

    frameProcessor = FrameProcessor(std_height, version)
    preprocessor = lambda _ : preprocessing(_, roi, rot_angle)
    
    def process_func(file_name):
        frameProcessor.set_image(file_name, preprocessor)
        output = frameProcessor.process_image_plain(ColorClassification().convert_to_01)
        return output 
    return process_func 

class Reader:
    def __init__(self, initial_exponent, screenshot_buffer, sleep_init = 1):
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
            if new_digits != last_digits:
                self.sleep_lag *= self.sleep_factor
            else: 
                print(new_digits)
            sleep(self.sleep_lag)
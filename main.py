from time import perf_counter, sleep
from datetime import timedelta

from logger import Logger
from takeAndroidScreenshot import takeScreenshot

from ImageProcessing import FrameProcessor

from color_classification import ColorClassification
from pre_process import preprocessing


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
    def __init__(self, initial_exponent, screenshot_buffer, sleep_init=1, minimum_lag=1):
        self.exponent = initial_exponent
        self.logger = Logger()
        self.sleep_factor = 1.1
        self.sleep_lag = sleep_init
        self.minimum_lag = minimum_lag
        self.screenshot_buffer = screenshot_buffer
        self.get_digit = getDigits()

    def turn_on_read(self):
        last_digits = "-1"
        while True:
            takeScreenshot(self.screenshot_buffer)
            new_digits = self.get_digit(self.screenshot_buffer)
            if len(new_digits) != 3: 
                print('-'*81)
                print("Failed to retrieve digits.")
                print("Attempt another retrival in %.1f s" %
                      (self.sleep_lag/2.))
                print('-'*81)
            if new_digits == last_digits:
                self.sleep_lag *= self.sleep_factor
                print('-'*81)
                print("No pressure change in the period.")
                print("Current sleep lag is changed into %.1f s" %
                      self.sleep_lag)
                print('-'*81)
                self.logger.log([perf_counter(), pressure])
            else:
                self.sleep_lag /= self.sleep_factor ** .5
                if self.sleep_lag < self.minimum_lag:
                    self.sleep_lag = self.minimum_lag
                pressure = self.cast_digits_to_number(last_digits, new_digits)
                if pressure == -1:
                    print('-'*81)
                    print("Failed to retrieve digits.")
                    print("Attempt another retrival in %.1f s" %
                        (self.sleep_lag/2.))
                    print('-'*81)
                    continue
                print('-'*81)
                print("New pressure of %.3e since %s elapsed, " % (
                    pressure,
                    str(timedelta(seconds=perf_counter()))
                ))
                print("Current sleep lag is %.1f s" % self.sleep_lag)
                print('-'*81)
                self.logger.log([perf_counter(), pressure])
                last_digits = new_digits
            sleep(self.sleep_lag)

    def cast_digits_to_number(self, old_digits, new_digits):
        """Given new and last digits, return the correct value
        """
        old = int(old_digits)
        new = int(new_digits)
        if abs(new - old) > 50:
            if (new * 10 - old) < 50:
                self.exponent -= 1
            elif (old * 10 - new) < 50: 
                self.exponent += 1
            else:
                return -1
        return new * 10 ** (self.exponent - 2)


reader = Reader(-5, "./1.png")
reader.turn_on_read()

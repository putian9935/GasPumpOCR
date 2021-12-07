import cv2
import time
import sys

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

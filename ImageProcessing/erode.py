import matplotlib.pyplot as plt
import cv2
import numpy as np

def remove_bridge(img):    
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.dilate(img, kernel, iterations=10)
    erosion[75:86,55:72] = 255
    
    return (cv2.erode(erosion, kernel, iterations=5)[...,0] == 0).astype(np.uint8)
    
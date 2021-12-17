__doc__ = """Since the camera is fixed, a simple crop of ROI would be fine
"""

from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2
import numpy as np
from PIL.PngImagePlugin import PngImageFile

def find_out_roi(img, roi=None):
    """
    Parameter
    ---------
    roi : a 4-element list of (left, upper, right, lower) coordinates
    """
    fig, ax = plt.subplots()
    ax.imshow(img)
    if not isinstance(roi, type(None)):
        ax.add_patch(Rectangle(roi[:2], roi[2]-roi[0],
                     roi[3]-roi[1], fill=False, edgecolor='red'))
    plt.show()


def rotate_image(image, angle):
    """Rotate an image (described by NumPy ndarray) by angle degree"""
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def preprocessing(img, roi, rot_angle=0):
    """Crop and rotate an image"""
    if type(img) == PngImageFile:
        return Image.fromarray(rotate_image(np.array(img.crop(roi)), rot_angle))
    else:
        return rotate_image(img[roi[1]:roi[3], roi[0]:roi[2], ], rot_angle)


if __name__ == '__main__':
    img = Image.open('1.png')
    find_out_roi(img, [677, 485, 1033, 677])
    plt.imshow(preprocessing(img,  [677, 485, 1033, 677], 1))
    plt.show()

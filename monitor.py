import screenshot
import numpy as np
import cv2
from PIL import ImageColor


class Monitor:
    def __init__(self, handle, debug, scaled_resolution):
        self.debug = debug
        self.handle = handle
        img = screenshot.get_image(handle, save=True)
        self.screen = np.fromstring(img[0], dtype='uint8')
        self.screen.shape = (img[1][1], img[1][0], 4)
        self.scaled_resolution = scaled_resolution
        self.screen = screenshot.resize(self.screen, scaled_resolution)

    def get_grayscale(self, image=None):
        if image is None:
            image = self.screen
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def show(self, image=None):
        if image is None:
            image = self.screen
        cv2.imshow('window', image)

    def update(self):
        img = screenshot.get_image(self.handle, save=False)
        self.screen = np.fromstring(img[0], dtype='uint8')
        self.screen.shape = (img[1][1], img[1][0], 4)
        self.screen = screenshot.resize(self.screen, self.scaled_resolution)

    def get_cords(self, match_img, gray_image=None, threshold=.9, poi=None, color='red'):
        if gray_image is None:
            gray_image = self.get_grayscale()
        res = cv2.matchTemplate(gray_image, match_img, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        cords = []
        if poi is not None:
            for pt in zip(*loc[::-1]):
                cords.append((pt[0], pt[1] + poi[0]))
        else:
            for pt in zip(*loc[::-1]):
                cords.append((pt[0], pt[1]))

        if self.debug:
            if cords.__len__() > 0:
                for c in cords:
                    self.debug_rectangle(c, match_img, ImageColor.getrgb(color))

        return cords

    def get_poi(self, start, end):
        return [int(self.screen.shape[0] * (start/100)), int(self.screen.shape[0] * (end / 100))]

    def get_template(self, template_name):
        return cv2.imread('resources/'+template_name, 0)

    def debug_rectangle(self, pt, match_img, color):
        w, h = match_img.shape[::-1]
        cv2.rectangle(self.screen, pt, (pt[0] + w, pt[1] + h), color, 2)





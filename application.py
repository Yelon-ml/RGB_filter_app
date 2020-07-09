import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class RGBApp:

    def __init__(self):
        self.image = cv.imread('img1.png')
        self.image_hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        self.image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.image_gray2 = cv.cvtColor(self.image_gray, cv.COLOR_GRAY2RGB)

    def mask_(self):
        blue_lower = np.array([100,150,0], np.uint8)
        blue_upper = np.array([140,255,255], np.uint8)
        self.mask = cv.inRange(self.image_hsv, blue_lower, blue_upper)
        self.mask2 = cv.bitwise_not(self.mask)

    def combine(self):
        self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask)
        self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask2)
        self.final = cv.addWeighted(self.comb2, 1, self.comb, 1, 0)


    def show(self, arg):
        cv.imshow('image', arg)
        cv.waitKey(0)
        #plt.axis('off')
        #plt.show()


app = RGBApp()
app.mask_()
app.image.shape
app.image_gray.shape
app.image_gray2.shape
app.combine()
app.show(app.final)

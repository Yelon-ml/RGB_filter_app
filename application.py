from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt






class RGBApp(Frame):

    def __init__(self, master, *args, **kwargs):

        self.root = master
        self.root.geometry("1008x50")
        self.root.configure(background="#6cb6eb")

        ### BUTTONS ###

        self.load_image_but = Button(self.root, text='Load Image', height=3, width=25, command=self.load_image)
        self.load_image_but.grid(row = 1, column = 1)
        self.red_but = Button(self.root, text='Red Filter', height=3, width=28)
        self.red_but.grid(row = 1, column = 2)
        self.green_but = Button(self.root, text='Green Filter', height=3, width=28, command=self.green_mask)
        self.green_but.grid(row = 1, column = 3)
        self.blue_but = Button(self.root, text='Blue Filter', height=3, width=28, command=self.blue_mask)
        self.blue_but.grid(row = 1, column = 4)
        self.quit_but = Button(self.root, text="Quit", height=3, width=28, command=quit)
        self.quit_but.grid(row=1, column=5)


    def load_image(self):
        self.x = filedialog.askopenfilename(title='Select the image')
        img = Image.open(self.x)
        img = img.resize((1004, 700), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 2, column=1, columnspan=5)
        self.load_image_but.config(text="Change Image")
        self.root.geometry("1008x760")

        self.image = cv.imread(os.path.basename(self.x))
        self.image_hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        self.image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.image_gray2 = cv.cvtColor(self.image_gray, cv.COLOR_GRAY2RGB)


    def blue_mask(self):
        self.panel.image = ""
        blue_lower = np.array([90,60,60], np.uint8)
        blue_upper = np.array([210,255,255], np.uint8)
        mask = cv.inRange(self.image_hsv, blue_lower, blue_upper)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((1, 1), np.uint8), iterations = 1)
        self.mask = cv.dilate(mask,np.ones((1, 1), np.uint8), iterations = 1)
        self.mask2 = cv.bitwise_not(self.mask)

        self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask)
        self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask2)

        self.final = cv.addWeighted(self.comb2, 1, self.comb, 1, 0)
        self.final = cv.resize(self.final, (1004, 700))
        self.final = cv.cvtColor(self.final, cv.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(self.final))
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 2, column=1, columnspan=5)

    def green_mask(self):
        self.panel.image = ""
        blue_lower = np.array([20,100,100], np.uint8)
        blue_upper = np.array([100,255,255], np.uint8)
        mask = cv.inRange(self.image_hsv, blue_lower, blue_upper)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((1, 1), np.uint8), iterations = 1)
        self.mask = cv.dilate(mask,np.ones((1, 1), np.uint8), iterations = 1)
        self.mask2 = cv.bitwise_not(self.mask)

        self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask)
        self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask2)

        self.final = cv.addWeighted(self.comb2, 1, self.comb, 1, 0)
        self.final = cv.resize(self.final, (1004, 700))
        self.final = cv.cvtColor(self.final, cv.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(self.final))
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 2, column=1, columnspan=5)


if __name__ == "__main__":
    root = Tk()
    App = RGBApp(root)
    root.title("RGB Filters Application")
    root.mainloop()

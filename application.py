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

        ##### BUTTONS #####

        ### 1st ROW ###

        self.load_image_but = Button(self.root, text='Load Image', height=3, width=25, command=self.load_image)
        self.load_image_but.grid(row = 1, column = 1)
        self.red_but = Button(self.root, text='Red Filter', height=3, width=28, command=lambda: self.red_mask("red"))
        self.red_but.grid(row = 1, column = 2)
        self.green_but = Button(self.root, text='Green Filter', height=3, width=28, command=lambda: self.green_mask("green"))
        self.green_but.grid(row = 1, column = 3)
        self.blue_but = Button(self.root, text='Blue Filter', height=3, width=28, command=lambda: self.blue_mask("blue"))
        self.blue_but.grid(row = 1, column = 4)
        self.quit_but = Button(self.root, text="Quit", height=3, width=28, command=quit)
        self.quit_but.grid(row=1, column=5)

        ### 2nd ROW ###

        self.original_but = Button(self.root, text='Original Image', height=3, width=25, command=self.original)
        self.original_but.grid(row = 2, column = 1)
        self.nored_but = Button(self.root, text='No Red', height=3, width=28, command=lambda: self.red_mask("nored"))
        self.nored_but.grid(row = 2, column = 2)
        self.nogreen_but = Button(self.root, text='No Green', height=3, width=28, command=lambda: self.green_mask("nogreen"))
        self.nogreen_but.grid(row = 2, column = 3)
        self.noblue_but = Button(self.root, text='No Blue', height=3, width=28, command=lambda: self.blue_mask("noblue"))
        self.noblue_but.grid(row = 2, column = 4)


        ##### FUNCTIONALITY #####


    def load_image(self):
        self.x = filedialog.askopenfilename(title='Select the image')
        img = Image.open(self.x)
        img = img.resize((1004, 700), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 3, column=1, columnspan=5)
        self.load_image_but.config(text="Change Image")
        self.root.geometry("1008x816")

        self.image = cv.imread(os.path.basename(self.x))
        self.image_hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        self.image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.image_gray2 = cv.cvtColor(self.image_gray, cv.COLOR_GRAY2RGB)

    def red_mask(self, arg):
        self.panel.image = ""
        red_lower1 = np.array([0,40,40], np.uint8)
        red_upper1 = np.array([15,255,255], np.uint8)
        red_lower2 = np.array([140,40,40], np.uint8)
        red_upper2 = np.array([180,255,255], np.uint8)
        mask1 = cv.inRange(self.image_hsv, red_lower1, red_upper1)
        mask2 = cv.inRange(self.image_hsv, red_lower2, red_upper2)
        mask = cv.bitwise_or(mask1, mask2)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((1, 1), np.uint8), iterations = 1)
        self.mask = cv.dilate(mask,np.ones((1, 1), np.uint8), iterations = 1)
        self.mask2 = cv.bitwise_not(self.mask)

        if arg == 'red':
            self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask)
            self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask2)
        if arg == 'nored':
            self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask2)
            self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask)

        self.final = cv.addWeighted(self.comb2, 1, self.comb, 1, 0)
        self.final = cv.resize(self.final, (1004, 700))
        self.final = cv.cvtColor(self.final, cv.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(self.final))
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 3, column=1, columnspan=5)

    def green_mask(self, arg):
        self.panel.image = ""
        green_lower = np.array([27,40,40], np.uint8)
        green_upper = np.array([92,255,255], np.uint8)
        mask = cv.inRange(self.image_hsv, green_lower, green_upper)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((1, 1), np.uint8), iterations = 1)
        self.mask = cv.dilate(mask,np.ones((1, 1), np.uint8), iterations = 1)
        self.mask2 = cv.bitwise_not(self.mask)

        if arg == 'green':
            self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask)
            self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask2)
        if arg == 'nogreen':
            self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask2)
            self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask)

        self.final = cv.addWeighted(self.comb2, 1, self.comb, 1, 0)
        self.final = cv.resize(self.final, (1004, 700))
        self.final = cv.cvtColor(self.final, cv.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(self.final))
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 3, column=1, columnspan=5)

    def blue_mask(self, arg):
        self.panel.image = ""
        blue_lower = np.array([95,50,50], np.uint8)
        blue_upper = np.array([140,255,255], np.uint8)
        mask = cv.inRange(self.image_hsv, blue_lower, blue_upper)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((1, 1), np.uint8), iterations = 1)
        self.mask = cv.dilate(mask,np.ones((1, 1), np.uint8), iterations = 1)
        self.mask2 = cv.bitwise_not(self.mask)

        if arg == 'blue':
            self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask)
            self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask2)
        if arg == 'noblue':
            self.comb = cv.bitwise_and(self.image, self.image, mask=self.mask2)
            self.comb2 = cv.bitwise_and(self.image_gray2, self.image_gray2, mask=self.mask)

        self.final = cv.addWeighted(self.comb2, 1, self.comb, 1, 0)
        self.final = cv.resize(self.final, (1004, 700))
        self.final = cv.cvtColor(self.final, cv.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(self.final))
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 3, column=1, columnspan=5)

    def original(self):
        self.panel.image = ""
        img = Image.open(self.x)
        img = img.resize((1004, 700), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.panel = Label(root, image = img)
        self.panel.image = img
        self.panel.grid(row = 3, column=1, columnspan=5)


if __name__ == "__main__":
    root = Tk()
    App = RGBApp(root)
    root.title("RGB Filters Application")
    root.mainloop()

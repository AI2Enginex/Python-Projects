
'''
    morphological operations application using opencv and tkinter.

    the operations mentioned in this application can be performed on 

    1. JPEG/PNG images.
    2. MP4 files.
    3. live camera. 
    
'''

import os
import cv2
import warnings
import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore", category=FutureWarning)

top = tk.Tk()
top.eval('tk::PlaceWindow . center')
canvas = tk.Canvas(top, width=400, height=200, background="light blue")
tk.Label(top, text="Morphological Operations",
         font=("Helvetica", 14), background="light blue").place(x=100, y=50)
canvas.pack()


def print_function(x):
    pass


class Image_processing:

    def __init__(self, input_image):

        self.image = cv2.resize(cv2.imread(input_image), (720, 700))
        self.events_clicked = []

    def click_event(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.image, (x, y), 3, (120, 120, 120), 4)
            self.events_clicked.append((x, y))
            if len(self.events_clicked) >= 2:
                cv2.line(
                    self.image, self.events_clicked[-1], self.events_clicked[-2], (120, 120, 120), 2)

            cv2.imshow("user image", self.image)

    def create_window(self):
        while True:
            hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            hue_lower_value = cv2.getTrackbarPos("hue", "image")
            satuaration_lower_value = cv2.getTrackbarPos("saturation", "image")
            brightness_lower_value = cv2.getTrackbarPos("value", "image")
            l_b = np.array(
                [hue_lower_value, satuaration_lower_value, brightness_lower_value])
            u_b = np.array([255, 255, 255])
            masked_image = cv2.inRange(hsv, l_b, u_b)
            image = cv2.bitwise_or(self.image, self.image, mask=masked_image)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            cv2.imshow("image", image)
        cv2.destroyAllWindows()

    def edge_detection(self):
        while True:
            grey_img = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            edge_intensity = cv2.getTrackbarPos("lower", "edge")
            edge_higher_intensity = cv2.getTrackbarPos("higher", "edge")
            edge_ = cv2.Canny(grey_img, edge_intensity, edge_higher_intensity)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            cv2.imshow("edge", edge_)
        cv2.destroyAllWindows()

    def countours(self):

        global countours
        while True:
            contour_image = self.image
            contour_image = cv2.resize(contour_image, (600, 512))
            gray = cv2.cvtColor(contour_image, cv2.COLOR_RGB2GRAY)

            gray_scale = cv2.getTrackbarPos("gray", "countours")
            color_scale = cv2.getTrackbarPos("color", "countours")

            _, binary = cv2.threshold(gray, gray_scale, 255, 0)
            countours, hierarchy = cv2.findContours(
                binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            all_countours = cv2.drawContours(
                contour_image, countours, -1, (color_scale, color_scale, color_scale), 7)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            cv2.imshow("countours", all_countours)
        cv2.destroyAllWindows()

    def image_thresholding(self):

        while True:
            image_blur = cv2.getTrackbarPos("blur", "image")
            image_brightness = cv2.getTrackbarPos("brightness", "image")

            get_, thresh = cv2.threshold(
                self.image, image_brightness, 300, cv2.THRESH_TRUNC)
            dst = cv2.blur(self.image, (image_blur, 2))

            brightness_ = cv2.addWeighted(thresh, 0.9, dst, 0.2, 0)
            cv2.imshow("image", brightness_)

            dst_ = cv2.addWeighted(dst, 0.9, thresh, 0.2, 0)
            cv2.imshow("image", dst_)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            cv2.imshow("image", self.image)
        cv2.destroyAllWindows()

    def check_frequency(self):
        while True:
            self.b, self.g, self.r = cv2.split(self.image)
            self.blue = cv2.getTrackbarPos("blue", "image")
            self.green = cv2.getTrackbarPos("green", "image")
            self.red = cv2.getTrackbarPos("red", "image")
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            cv2.imshow("image", self.image)
        cv2.destroyAllWindows()

    def display_graph(self):
        self.check_frequency()
        plt.hist(self.b.ravel(), 100, [0, self.blue], color='blue')
        plt.hist(self.g.ravel(), 100, [0, self.green], color='green')
        plt.hist(self.r.ravel(), 100, [0, self.red], color='red')
        plt.show()


class Create_video:

    def gray_scale(self, image):
        self.gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def print_function(self, x):
        print(x)

    def canny_edge(self, image):

        self.gray_scale(image)
        low = cv2.getTrackbarPos("low", "edges")
        high = cv2.getTrackbarPos("high", "edges")
        canny = cv2.Canny(self.gray, low, high)
        return canny

    def hsv_color(self, image):

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hue_lower_value = cv2.getTrackbarPos("hue", "image")
        satuaration_lower_value = cv2.getTrackbarPos("saturation", "image")
        brightness_lower_value = cv2.getTrackbarPos("value", "image")
        l_b = np.array(
            [hue_lower_value, satuaration_lower_value, brightness_lower_value])
        u_b = np.array([255, 255, 255])
        masked_image = cv2.inRange(hsv, l_b, u_b)
        image = cv2.bitwise_or(image, image, mask=masked_image)
        return image

    def contours(self, image):
        while True:
            contour_image = image
            contour_image = cv2.resize(contour_image, (600, 512))
            gray = cv2.cvtColor(contour_image, cv2.COLOR_RGB2GRAY)

            gray_scale = cv2.getTrackbarPos("gray", "countours")
            color_scale = cv2.getTrackbarPos("color", "countours")

            _, binary = cv2.threshold(gray, gray_scale, 255, 0)
            countours, hierarchy = cv2.findContours(
                binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            all_countours = cv2.drawContours(
                contour_image, countours, -1, (color_scale, color_scale, color_scale), 7)

            return all_countours

    def display_graph(self):

        plt.hist(self.b.ravel(), 100, [0, self.blue], color='blue')
        plt.hist(self.g.ravel(), 100, [0, self.green], color='green')
        plt.hist(self.r.ravel(), 100, [0, self.red], color='red')
        plt.show()


class CameraObjects:

    @classmethod
    def edge_detection(cls):
        return cv2.VideoCapture(0)

    @classmethod
    def hsv_color_camera(cls):

        return cv2.VideoCapture(0)

    @classmethod
    def contour(cls):

        return cv2.VideoCapture(0)

    @classmethod
    def color_frequency(cls):

        return cv2.VideoCapture(0)


class Display_video(CameraObjects, Create_video):

    def edge(self):

        edge_obj = CameraObjects().edge_detection()

        while True:
            frame, cap = edge_obj.read()
            if frame:
                cv2.imshow('edges', self.canny_edge(cap))
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break

        edge_obj.release()
        cv2.destroyAllWindows()

    def hsv_color_space(self):

        hsv_color_ = CameraObjects().hsv_color_camera()
        while True:

            frame, cap = hsv_color_.read()
            if frame:
                cv2.imshow("image", self.hsv_color(cap))
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break

        hsv_color_.release()
        cv2.destroyAllWindows()

    def video_countour(self):

        vc = CameraObjects().contour()
        while True:

            frame, cap = vc.read()
            if frame:
                cv2.imshow("countours", self.contours(cap))
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break

        vc.release()
        cv2.destroyAllWindows()

    def color_frequency(self):

        freq = CameraObjects().color_frequency()
        while True:

            frame, cap = freq.read()

            self.b, self.g, self.r = cv2.split(cap)
            self.blue = cv2.getTrackbarPos("blue", "image")
            self.green = cv2.getTrackbarPos("green", "image")
            self.red = cv2.getTrackbarPos("red", "image")

            if frame:

                cv2.imshow("image", cap)

                key = cv2.waitKey(1)
                if key == ord('q'):

                    break

            else:
                break

        freq.release()
        cv2.destroyAllWindows()
        self.display_graph()


class Video_files:

    def gray_scale(self, image):
        self.gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def print_function(self, x):
        print(x)

    def canny_edge(self, image):

        self.gray_scale(image)
        low = cv2.getTrackbarPos("low", "edges")
        high = cv2.getTrackbarPos("high", "edges")
        canny = cv2.Canny(self.gray, low, high)
        return canny

    def hsv_color(self, image):

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hue_lower_value = cv2.getTrackbarPos("hue", "image")
        satuaration_lower_value = cv2.getTrackbarPos("saturation", "image")
        brightness_lower_value = cv2.getTrackbarPos("value", "image")
        l_b = np.array(
            [hue_lower_value, satuaration_lower_value, brightness_lower_value])
        u_b = np.array([255, 255, 255])
        masked_image = cv2.inRange(hsv, l_b, u_b)
        image = cv2.bitwise_or(image, image, mask=masked_image)
        return image

    def contours(self, image):
        while True:
            contour_image = image

            contour_image = cv2.resize(contour_image, (600, 512))

            gray = cv2.cvtColor(contour_image, cv2.COLOR_RGB2GRAY)

            gray_scale = cv2.getTrackbarPos("gray", "countours")
            color_scale = cv2.getTrackbarPos("color", "countours")
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            _, binary = cv2.threshold(blur, gray_scale, 255, cv2.THRESH_BINARY)
            dilated_image = cv2.dilate(binary, None, iterations=3)
            countours, hierarchy = cv2.findContours(
                dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            all_countours = cv2.drawContours(
                contour_image, countours, -1, (color_scale, color_scale, color_scale), 7)

            return all_countours

    def display_graph(self):

        plt.hist(self.b.ravel(), 100, [0, self.blue], color='blue')
        plt.hist(self.g.ravel(), 100, [0, self.green], color='green')
        plt.hist(self.r.ravel(), 100, [0, self.red], color='red')
        plt.show()


class Display_video_files(Video_files):

    def __init__(self, video):

        self.video = cv2.VideoCapture(video)

    def edge(self):
        while True:
            frame, cap = self.video.read()
            if frame:
                cv2.imshow('edges', self.canny_edge(cap))
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break
        self.video.release()
        cv2.destroyAllWindows()

    def hsv_color_space(self):

        while True:

            frame, cap = self.video.read()
            if frame:
                cv2.imshow("image", self.hsv_color(cap))
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break
        self.video.release()

        cv2.destroyAllWindows()

    def video_countour(self):

        while True:

            frame, cap = self.video.read()
            if frame:
                cv2.imshow("countours", self.contours(cap))
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break
        self.video.release()
        cv2.destroyAllWindows()

    def color_frequency(self):

        while True:

            frame, cap = self.video.read()

            self.b, self.g, self.r = cv2.split(cap)
            self.blue = cv2.getTrackbarPos("blue", "image")
            self.green = cv2.getTrackbarPos("green", "image")
            self.red = cv2.getTrackbarPos("red", "image")

            if frame:

                cv2.imshow("image", cap)

                key = cv2.waitKey(1)
                if key == ord('q'):

                    break
            else:
                break

        self.video.release()

        cv2.destroyAllWindows()
        self.display_graph()


if __name__ == "__main__":

    def image_processing():

        image_canvas = tk.Tk()
        canvas_default_image = tk.Canvas(
            image_canvas, width=400, height=300, background="light green")

        tk.Label(image_canvas, text="Enter name of image",
                 background="light green").place(x=60, y=50)
        entry = tk.Entry(image_canvas)
        canvas_default_image.create_window(250, 60, window=entry)

        canvas_default_image.pack()

        def hsv():

            value = entry.get()
            if os.path.exists(value):
                im = Image_processing(value)
                cv2.namedWindow("image")
                cv2.createTrackbar("hue", "image", 0, 250, print_function)
                cv2.createTrackbar("saturation", "image",
                                   0, 250, print_function)
                cv2.createTrackbar("value", "image", 0, 250, print_function)
                im.create_window()
            else:
                messagebox.showwarning(title="Error", message="file not found")

        def mouse_envent():
            value = entry.get()
            if os.path.exists(value):
                im = Image_processing(value)
                user_image = im.image
                cv2.imshow("user image", user_image)
                cv2.setMouseCallback("user image", im.click_event)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                messagebox.showwarning(title="Error", message="file not found")

        def edge():

            value = entry.get()
            if os.path.exists(value):
                im = Image_processing(value)
                cv2.namedWindow("edge")
                cv2.createTrackbar("lower", "edge", 0, 250, print_function)
                cv2.createTrackbar("higher", "edge", 0, 250, print_function)
                im.edge_detection()
            else:
                messagebox.showwarning(title="Error", message="file not found")

        def outlines():
            value = entry.get()
            if os.path.exists(value):
                im = Image_processing(value)
                cv2.namedWindow("countours")
                cv2.createTrackbar("gray", "countours", 0, 255, print_function)
                cv2.createTrackbar("color", "countours",
                                   0, 255, print_function)
                im.countours()
            else:
                messagebox.showwarning(title="Error", message="file not found")

        def color_frequency():
            value = entry.get()
            if os.path.exists(value):
                im = Image_processing(value)
                cv2.namedWindow("image")
                cv2.createTrackbar("blue", "image", 0, 256, print_function)
                cv2.createTrackbar("green", "image", 0, 256, print_function)
                cv2.createTrackbar("red", "image", 0, 256, print_function)
                im.display_graph()
            else:
                messagebox.showwarning(title="Error", message="file not found")

        def img_threshold():
            value = entry.get()
            if os.path.exists(value):
                im = Image_processing(value)
                cv2.namedWindow("image")
                cv2.createTrackbar("brightness", "image",
                                   0, 300, print_function)
                cv2.createTrackbar("blur", "image", 1, 10, print_function)
                im.image_thresholding()
            else:
                messagebox.showwarning(title="Error", message="file not found")

        tk.Button(image_canvas, text="hsv color space", bg='white',
                  fg='Black', command=hsv).place(x=80, y=180)
        tk.Button(image_canvas, text="event handler", bg='white',
                  fg='Black', command=mouse_envent).place(x=80, y=100)
        tk.Button(image_canvas, text="edge detection", bg='white',
                  fg='Black', command=edge).place(x=80, y=140)
        tk.Button(image_canvas, text="countour analysis", bg='white',
                  fg='Black', command=outlines).place(x=220, y=140)
        tk.Button(image_canvas, text="frequency Analysis", bg='white',
                  fg='Black', command=color_frequency).place(x=220, y=180)
        tk.Button(image_canvas, text="image-brightness", bg='white',
                  fg='Black', command=img_threshold).place(x=220, y=100)

        image_canvas.mainloop()

    def web_camera():

        image_canvas = tk.Tk()

        canvas_default_image = tk.Canvas(
            image_canvas, width=400, height=300, background="light green")
        tk.Label(image_canvas, text="Requires Web Camera Driver",
                 font=("Helvetica", 12), background="light green").place(x=100, y=50)
        canvas_default_image.pack()
        dv = Display_video()

        def web_camera_edge():

            cv2.namedWindow("edges")
            cv2.createTrackbar("low", "edges", 0, 255, dv.print_function)
            cv2.createTrackbar("high", "edges", 0, 255, dv.print_function)

            dv.edge()

        def web_camera_contours():

            cv2.namedWindow("countours")
            cv2.createTrackbar("gray", "countours", 0, 255, dv.print_function)
            cv2.createTrackbar("color", "countours", 0, 255, dv.print_function)
            dv.video_countour()

        def camera_hsv():

            cv2.namedWindow("image")
            cv2.createTrackbar("hue", "image", 0, 250, dv.print_function)
            cv2.createTrackbar("saturation", "image", 0,
                               250, dv.print_function)
            cv2.createTrackbar("value", "image", 0, 250, dv.print_function)
            dv.hsv_color_space()

        def web_color_frequency():

            cv2.namedWindow("image")
            cv2.createTrackbar("blue", "image", 0, 256, dv.print_function)
            cv2.createTrackbar("green", "image", 0, 256, dv.print_function)
            cv2.createTrackbar("red", "image", 0, 256, dv.print_function)

            dv.color_frequency()

        tk.Button(image_canvas, text="Edge Detection", bg='white',
                  fg='Black', command=web_camera_edge).place(x=80, y=180)
        tk.Button(image_canvas, text="video countours", bg='white',
                  fg='Black', command=web_camera_contours).place(x=80, y=100)
        tk.Button(image_canvas, text="hsv color space", bg='white',
                  fg='Black', command=camera_hsv).place(x=220, y=180)
        tk.Button(image_canvas, text="color frequency", bg='white',
                  fg='Black', command=web_color_frequency).place(x=220, y=100)
        image_canvas.mainloop()

    def video_files():

        image_canvas = tk.Tk()
        canvas_default_image = tk.Canvas(
            image_canvas, width=400, height=300, background="light green")

        tk.Label(image_canvas, text="Enter a video file name",
                 background="light green").place(x=60, y=50)
        entry = tk.Entry(image_canvas)
        canvas_default_image.create_window(250, 60, window=entry)

        canvas_default_image.pack()

        def web_camera_edge():
            value = entry.get()
            if os.path.exists(value):
                dvf = Display_video_files(value)
                cv2.namedWindow("edges")
                cv2.createTrackbar("low", "edges", 0, 255, dvf.print_function)
                cv2.createTrackbar("high", "edges", 0, 255, dvf.print_function)
                dvf.edge()
            else:
                messagebox.showerror(title="Error", message="file not found")

        def web_camera_contours():

            value = entry.get()
            if os.path.exists(value):
                dvf = Display_video_files(value)
                cv2.namedWindow("countours")
                cv2.createTrackbar("gray", "countours", 0,
                                   255, dvf.print_function)
                cv2.createTrackbar("color", "countours", 0,
                                   255, dvf.print_function)
                dvf.video_countour()
            else:
                messagebox.showerror(title="Error", message="file not found")

        def camera_hsv():
            value = entry.get()
            if os.path.exists(value):

                dvf = Display_video_files(value)
                cv2.namedWindow("image")
                cv2.createTrackbar("hue", "image", 0, 250, dvf.print_function)
                cv2.createTrackbar("saturation", "image", 0,
                                   250, dvf.print_function)
                cv2.createTrackbar("value", "image", 0,
                                   250, dvf.print_function)
                dvf.hsv_color_space()
            else:
                messagebox.showerror(title="Error", message="file not found")

        def web_color_frequency():
            value = entry.get()
            if os.path.exists(value):
                dvf = Display_video_files(value)
                cv2.namedWindow("image")
                cv2.createTrackbar("blue", "image", 0, 256, dvf.print_function)
                cv2.createTrackbar("green", "image", 0,
                                   256, dvf.print_function)
                cv2.createTrackbar("red", "image", 0, 256, dvf.print_function)
                dvf.color_frequency()
            else:
                messagebox.showerror(title="Error", message="file not found")

        tk.Button(image_canvas, text="Edge Detection", bg='white',
                  fg='Black', command=web_camera_edge).place(x=80, y=180)
        tk.Button(image_canvas, text="video countours", bg='white',
                  fg='Black', command=web_camera_contours).place(x=80, y=100)
        tk.Button(image_canvas, text="hsv color space", bg='white',
                  fg='Black', command=camera_hsv).place(x=220, y=180)
        tk.Button(image_canvas, text="color frequency", bg='white',
                  fg='Black', command=web_color_frequency).place(x=220, y=100)

        image_canvas.mainloop()

    canvas.create_window(100, 120, window=tk.Button(
        text="non-camera", command=image_processing))
    canvas.create_window(200, 120, window=tk.Button(
        text="web-camera", command=web_camera))
    canvas.create_window(300, 120, window=tk.Button(
        text="select a video", command=video_files))

    top.mainloop()

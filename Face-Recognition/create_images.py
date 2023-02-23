
import os
import cv2
import numpy as np 
import tkinter as tk
from tkinter import messagebox

class Record_Camera:

    def __init__(self, folder,name_of_person):

        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier("D:/CNN_Projects/face detection/haarcascade_frontalface_default.xml")
        self.skip = 0
        self.face_data = []
        self.dataset_path = folder

        self.file_name = name_of_person

    def record_face(self):
        
        while True:
            ret,frame = self.cap.read()
            gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            if ret == False:
                continue
            faces = self.face_cascade.detectMultiScale(gray_frame,1.3,5)
            
            if len(faces) == 0:
                continue
            k = 1

            faces = sorted(faces, key = lambda x : x[2]*x[3] , reverse = True)
            self.skip += 1

            for face in faces[:1]:
                x,y,w,h = face
                offset = 5
                face_offset = frame[y-offset:y+h+offset,x-offset:x+w+offset]
                face_selection = cv2.resize(face_offset,(100,100))
                if self.skip % 10 == 0:
                    self.face_data.append(face_selection)

                cv2.imshow(str(k), face_selection)
                k += 1
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.imshow("faces",frame)
            key_pressed = cv2.waitKey(1) & 0xFF 
            if key_pressed == ord('q'):
                break

        face_data = np.array(self.face_data)
        face_data = face_data.reshape((face_data.shape[0], -1))

        np.save(self.dataset_path + self.file_name, face_data)
        self.cap.release()
        cv2.destroyAllWindows()

class Image_canvas:

    def __init__(self):

        self.top = tk.Tk()
        self.canvas = tk.Canvas(self.top, width=400, height=200 , background="light blue")
        self.top.eval('tk::PlaceWindow . center')
        tk.Label(self.top, text="Create Dataset",font=("Helvetica", 14) , background="light blue").place(x=127, y=30)
        tk.Label(self.top, text="Enter Path for Folder : ",font=("Helvetica", 10) , background="light blue").place(x=50, y=77)
        tk.Label(self.top, text="Enter Name of Person : ",font=("Helvetica", 10) , background="light blue").place(x=50, y=110)

        self.entry_widget = tk.Entry(self.top)
        self.name_widget = tk.Entry(self.top)
        self.canvas.create_window(250, 87, window=self.entry_widget)
        self.canvas.create_window(254, 120, window=self.name_widget)
        self.canvas.pack()


    def run_app(self):

        def run_code():
            try:
                entry_value = self.entry_widget.get()
                name_value = self.name_widget.get()
                if os.path.exists(entry_value):
                    rc = Record_Camera(folder=entry_value,name_of_person=name_value)
                    rc.record_face()
                else:
                    messagebox.showwarning(title="Error",message="worng folder path")
            except Exception:

                messagebox.showwarning(title="Error",message="camera not found")
                
                
        
        tk.Button(self.top, text="Capture Face", bg='white',
                  fg='Black', command=run_code).place(x=160, y=150)
        self.top.mainloop()

if __name__ == "__main__":

    ic = Image_canvas()
    ic.run_app()
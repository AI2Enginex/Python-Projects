
import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox


class Algorithm:

    def __init__(self):
        pass

    def distance(self,v1, v2):
        return np.sqrt(((v1-v2)**2).sum())
    
    def knn(self,train, test, k=5):
        dist = []
        for i in range(train.shape[0]):
            ix = train[i, :-1]
            iy = train[i, -1]
            d = self.distance(test, ix)
            dist.append([d, iy])

        dk = sorted(dist, key=lambda x: x[0])[:k]
        labels = np.array(dk)[:, -1]
        output = np.unique(labels, return_counts=True)
        index = np.argmax(output[1])

        return output[0][index]
    
class Face_Recognition:

    def __init__(self,path):

        self.algo = Algorithm()
        self.face_data = []
        self.labels = []
        self.class_id = 0
        self.names = {}
        self.dataset_path = path
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier("D:/CNN_Projects/face detection/haarcascade_frontalface_default.xml")


    def create_array(self):
        
        for fx in os.listdir(self.dataset_path):
            if fx.endswith('.npy'):
                self.names[self.class_id] = fx[:-4]
                data_item = np.load(self.dataset_path + fx)
                self.face_data.append(data_item)
                target = self.class_id * np.ones((data_item.shape[0],))
                self.class_id += 1
                self.labels.append(target)
        face_dataset = np.concatenate(self.face_data, axis=0)
        face_labels = np.concatenate(self.labels, axis=0).reshape((-1, 1))
        self.trainset = np.concatenate((face_dataset, face_labels), axis=1)
        
        
    def display_frame(self):

        self.create_array()
        while True:
            ret, frame = self.cap.read()
            if ret == False:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for face in faces:
                x, y, w, h = face
                offset = 5
                face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
                face_section = cv2.resize(face_section, (100, 100))
                out = self.algo.knn(self.trainset, face_section.flatten())
                cv2.putText(frame, self.names[int(out)],(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)

            cv2.imshow("Faces", frame)
            cv2.moveWindow("Faces", 400,60)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

class Image_canvas:

    def __init__(self):

        self.top = tk.Tk()
        self.canvas = tk.Canvas(self.top, width=400, height=200 , background="light blue")
        self.top.eval('tk::PlaceWindow . center')
        tk.Label(self.top, text="Select Folder",font=("Helvetica", 14) , background="light blue").place(x=127, y=50)
        tk.Label(self.top, text="Enter Path for Folder : ",font=("Helvetica", 10) , background="light blue").place(x=50, y=87)
        self.entry_widget = tk.Entry(self.top)
        self.canvas.create_window(250, 100, window=self.entry_widget)
        self.canvas.pack()


    def run_app(self):

        def run_code():

            entry_value = self.entry_widget.get() 
            if os.path.exists(entry_value):
                try:
                    fc = Face_Recognition(entry_value)
                    fc.display_frame()
                except Exception:
                    messagebox.showwarning(title="Error",message="add a forward  slash in the end")

            else:

                messagebox.showwarning(title="Error",message="folder not found")
                
                
        
        tk.Button(self.top, text="Detect Frame", bg='white',
                  fg='Black', command=run_code).place(x=160, y=120)
        self.top.mainloop()


if __name__ == "__main__":

    ic = Image_canvas()
    ic.run_app()


        

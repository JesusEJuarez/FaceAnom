import tkinter as tk
from tkinter import filedialog

import cv2
import mediapipe as mp
from PIL import Image
from PIL import ImageTk
import imutils

"""
Reference 
https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_detection.md
https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_detection.md#model_selection
https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a85b55cf6a4a50451367ba96b65218ba1
https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html 
https://omes-va.com/tkinter-opencv-video/ 

"""
def upload_video():
    record_button.config(state = 'disabled')
    upload_button.config(state = 'disabled')
    open_button.config(state = 'disabled')
    
    #This funtions is used to open a video file
    file_path = filedialog.askopenfilename()
    mp_face = import_model()
    if file_path:
       

        video = cv2.VideoCapture(file_path) # Loads the video
        ret, frame = video.read() # returns video Frames
        output_video = cv2.VideoWriter(output_file_name,
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       25,
                                       (frame.shape[1], frame.shape[0]))

        while ret:
            frame = process_img(frame, mp_face)

            output_video.write(frame)

            ret, frame = video.read()

        video.release()
        output_video.release()

    record_button.config(state = 'normal')
    upload_button.config(state = 'normal')
    open_button.config(state = 'normal')

def record_video():
    global is_recording
    if is_recording:
        upload_button.config(state='disabled')
        open_button.config(state='disabled')
        global cap 
        global mp_face 
        global output_video

        record_button.config(text = "Stop")
        cap = cv2.VideoCapture(0)
        mp_face = import_model()
        output_video = cv2.VideoWriter(output_file_name,
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       25,
                                       (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        
        visualizar()
    else:
        record_button.config(text = "Record Video")
        cap.release()
        output_video.release()
        upload_button.config(state='normal')
        open_button.config(state='normal')

    is_recording = not is_recording
def visualizar():
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = process_img(frame, mp_face)
            output_video.write(frame)

            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(15, visualizar)
        else:
            lblVideo.image = ""
            cap.release()
def import_model():
    mp_face = mp.solutions.face_detection.FaceDetection(
        model_selection = 1, #Model selection
        min_detection_confidence = 0.5 #Condidence threshold
    )
    return mp_face
def process_img(frame, mp_face):
    HIGH, WEIGHT, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out = mp_face.process(frame_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
            x1 = int(x1 * WEIGHT)
            y1 = int(y1 * HIGH)
            w = int(w * WEIGHT)
            h = int(h * HIGH)

            # blur faces
            frame[y1:y1 + h, x1:x1 + w, :] = cv2.blur(frame[y1:y1 + h, x1:x1 + w, :], (30, 30)) # blur faces

    return frame
def output_file():
    global output_file_name
    filetypes = [('Video files', '*.MP4'), ('All files', '*.*')]
    output_file_name = filedialog.asksaveasfilename(title='Save as...', filetypes=filetypes, defaultextension='.mp4')
    upload_button.config(state='normal')
    record_button.config(state='normal')

is_recording = True
state = "disabled" 

# Start main window
root = tk.Tk()
root.title("Face-Anom") # Window title
root.geometry("840x700") # Window dimension
root.configure(bg = "#b9f252")  # Background color

root.grid_rowconfigure(1, weight=1)  # Adjust row 1 to take extra vertical space
root.grid_columnconfigure(0, weight=1)  # Adjust column 0 to take extra horizontal space

#Make tittle 
title_label = tk.Label(
                    root, 
                    text = "FACE-ANOM", 
                    font = ("Helvetica", 18, "bold"),
                    bg = "#b9f252",
                    )
title_label.grid(row = 0, column = 0, pady = 5, sticky = "n")

instructions = ( 
    "Instructions: This desktop app allows you to anonymize faces in a video: \n \n "
    "+ Firt use 'Choose destination file name' to select where you want to save the anom-video. \n"
    "+ Use 'Upload Video' to load a video from your computer. \n"
    "+ Use 'Record Video' to capture a video from your webcam. \n"
    "+ The app will automatically blur detected faces. \n"
    )

instructions_label = tk.Label(root, 
                              text=instructions, 
                              wraplength = 500,
                              font = ("Helvetica", 12),
                              bg="#7ba03a",
                              fg="#555"
                              )
instructions_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "n")


#Make buttons 
buttons_frame = tk.Frame(root, bg = "#7ba03a")
buttons_frame.grid(row=2, column=0, pady = 5, sticky = "nsew")

buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)

open_button = tk.Button(buttons_frame, bg = "#ddd", text = "Choose destination file name", command =  output_file)
open_button.grid(row = 0, column = 0, columnspan = 2, padx = 10,  pady = 5, sticky = "ew")

upload_button = tk.Button(buttons_frame, bg = "#ddd", text = "Upload Video", width = 20, command = upload_video, state = state)
upload_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "ew")

record_button = tk.Button(buttons_frame, bg = "#ddd", text = "Record Video", width = 20, command = record_video, state = state)
record_button.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "ew")

#Video Window
lblVideo = tk.Label(buttons_frame,  bg = "#ddd", width = 540 , height = 600)
lblVideo.grid(column = 0, row = 2, columnspan = 2, pady = 20, sticky = "snew")

# Make footer

footer_label = tk.Label(root, bg = "#092904", text = "CS50 Final Project", font = ("Helvetica", 10, "italic"))
footer_label.grid(row=3, column=0, pady=20, sticky="s")

root.mainloop()
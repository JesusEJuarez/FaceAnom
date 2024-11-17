import tkinter as tk
from tkinter import filedialog

import cv2
import mediapipe as mp


"""
Reference 
https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_detection.md
https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_detection.md#model_selection
https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a85b55cf6a4a50451367ba96b65218ba1
https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html 
https://omes-va.com/tkinter-opencv-video/ 

"""
def upload_video():
    #This funtions is used to open a video file
    file_path = filedialog.askopenfilename()
    mp_face = import_model()
    if file_path:
        video = cv2.VideoCapture(file_path) # Loads the video
        ret, frame = video.read() # returns video Frames
        output_video = cv2.VideoWriter('./output/output.mp4',
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       25,
                                       (frame.shape[1], frame.shape[0]))

        while ret:
            frame = process_img(frame, mp_face)

            output_video.write(frame)

            ret, frame = video.read()

        video.release()
        output_video.release()



def record_video():
    global is_recording
    if is_recording:
        record_button.config(text = "Stop")

    else:
        record_button.config(text = "Record Video")

    is_recording = not is_recording

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

is_recording = False
# Start main window
root = tk.Tk()
root.title("Face-Anom")
root.geometry("640x500") 

#Make tittle 
title_label = tk.Label(root, text = "FACE-ANOM", font = ("Helvetica", 16, "bold"))
title_label.pack(pady=5)

instructions = ( 
    "Instructions: This desktop app allows you to anonymize faces in a video: \n "
    "+ Use 'Upload Video' to load a video from your computer. \n"
    "+ Use 'Record Video' to capture a video from your webcam. \n"
    "+ The app will automatically blur detected faces. \n"
    )

instructions_label = tk.Label(root, text=instructions, justify="left", wraplength=350)
instructions_label.pack(pady=5)
#Make buttons 
buttos_frame = tk.Frame(root)
buttos_frame.pack(pady = 5 )


upload_button = tk.Button(buttos_frame, text = "Upload Video", width = 20, command = upload_video)
upload_button.grid(row = 0, column = 0, padx = 10, pady = 5)

record_button = tk.Button(buttos_frame, text = "Record Video", width = 20, command = record_video)
record_button.grid(row = 0, column = 1, padx = 10, pady = 5)

#Video Window
lblVideo = tk.Label(buttos_frame)
lblVideo.grid(column = 0, row = 1, columnspan = 2)

# Make footer

footer_label = tk.Label(root, text = "CS50 Final Project", font = ("Helvetica", 10, "italic"))
footer_label.pack(side = "bottom", pady = 20)

root.mainloop()
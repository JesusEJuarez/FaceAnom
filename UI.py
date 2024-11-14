import tkinter as tk
from tkinter import filedialog

def upload_video():
    """This funtions is used to open a video file, and then anonimaizer"""
    file_path = filedialog.askopenfilename()
    if file_path:
        pass
def record_video():
    pass


# Start main window
root = tk.Tk()
root.title("Face-Anom")
root.geometry("400x300") 

#Make tittle 
title_label = tk.Label(root, text = "FACE-ANOM", font = ("Helvetica", 16, "bold"))
title_label.pack(pady=10)

instructions = ( 
    "Instructions: This desktop app allows you to anonymize faces in a video: "
    "+ Use 'Upload Video' to load a video from your computer."
    "+ Use 'Record Video' to capture a video from your webcam."
    "+ The app will automatically blur detected faces."
    )


#Make buttons 
buttos_frame = tk.Frame(root)
buttos_frame.pack(pady = 20 )


upload_button = tk.Button(buttos_frame, text = "Upload Video", width = 20, command = upload_video)
upload_button.grid(row = 0, column = 0, padx = 10, pady = 10)

record_button = tk.Button(buttos_frame, text = "Record Video", width = 20, command = record_video)
record_button.grid(row = 0, column = 1, padx = 10, pady = 10)

# Make footer

footer_label = tk.Label(root, text = "CS50 Final Project", font = ("Helvetica", 10, "italic"))
footer_label.pack(side = "bottom", pady = 10)

root.mainloop()
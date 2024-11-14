import tkinter as tk
from tkinter import filedialog

def upload_video():
    """This funtions is used to open a video file, and then anonimaizer"""
    file_path = filedialog.askopenfilename()
    if file_path:
        
def record_video():
    pass

root = tk.Tk()
root.title("Video Face-Privacy")

upload_button = tk.Button(root, text = "Upload Video", command = upload_video)
upload_button.pack(pady=20) 

record_button = tk.Button(root, text = "Record Video", command = record_video)
record_button.pack(pady=20)


root.mainloop()
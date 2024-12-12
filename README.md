# FACE-ANOM
#### Video Demo:  <https://youtu.be/ef8cEhDPXPc>
#### Description:
Face-Anom is a desktop application designed to anonymize faces in videos by applying a blur effect to detected faces. The app supports two modes:

* Upload a pre-recorded video for processing.
* Record a video using your webcam.
Built using Python, OpenCV, and MediaPipe, this project is part of a final project for CS50

**Features**
* Face detecion and anonymization: Using google API, automatically detects faces in video and applies blur effect to anonymize them
* Video upload and Recording: Process existing videos or record videos using webcam
* Real- time Visualizations: See you video while recording 

**Instructions**

**GUI Overview**
* Title: the app name: "FACE-ANOM"
* Instrucions Panel: Provides a quick guide 
* Buttos: 
    + Choose Destination File Name: Specify the output video file name
    + Upload Video: Select a pre-recorded video to process.
    + Record Video: Start or stop recording from webcam
* Display the live video while recording 


**Technical Details**
1. Face detection:
    The aplication uses MediaPipe, an open-source framework by google, for computer vision task.
    This program uses the MediaPipe Face Detection Solution, which is a model for human face detection in images.
    * Model Selection: This parametrer is used to select the model in this app model_selections=1
    * Confidence: Confidence Threshold: This parameter ensures that only detected with a confidence of 50% or higher are processed. So false positives are reduced.
2. Image Processing:
    The detected faces are blurred: The process is:
    + Converting the frame from BGR (default in OpenCV) to RGB, which is required by MediaPipe
    + Processing the frame using MediaPipe's face detection model to identify bounding boxes
    around faces.
    + Extracting the bounding box coordinates, which are provided as normalized values.
    + Applaying a Blur over the bounding box area of each detected face. Using OpenCV's cv2.blur()
3. Video Processing:
    * Video input:
        * For uploaded vieos, is used cv2.VideoCapture() to read frames sequentially.
        * For webcam recording, the app streams live video using the same method.
    * Frame by frame processing: 
        Each frame is passed though the process_img() funtions to detect and blur faces before writing the processed frame to the output video.
    * Video Output:
        The cv2.VideoWriter() is used to save the processed video.
    * Real-Time video Display:
        The app uses Pillow and Tkinter to render processed frames in the GUI.
4. Graphical User Interface (GUI): The GUI is built using TKinter.
    * Responsiveness: The layout uses grid configurations with weight distribution to adapt.
5. File Handling:
    * Input Videos: Users can select a video file to process
    * Output Videos: Users specify the destination filename and locations

**Reference**
* [MediaPipe Face Detetion](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_detection.md): From here I get the documentation to learn how to use google API.
* OpenCV Documentation: Documentaion to learn image processing with openCV
    + [OpenCV VideoCapture Documentation](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html)
    + [OpenCV VideoWriter Documentation](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html)
    + [OpenCV Blur Documentation](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) 
* [Tkinter and OpenCV Integration](https://omes-va.com/tkinter-opencv-video/): From here I learn to show video on Tkinter GUI.

